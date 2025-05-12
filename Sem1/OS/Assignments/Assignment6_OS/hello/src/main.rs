use std::{
    fs,
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
    sync::{
        atomic::{AtomicBool, Ordering},
        mpsc, Arc, Mutex,
    },
    thread,
    time::Duration,
};

use ctrlc; // Add ctrlc = "3.2" (or latest) to Cargo.toml

pub type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<Worker>,
    senders: Vec<mpsc::Sender<Job>>,
    next: Mutex<usize>,
}

impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0, "ThreadPool size must be greater than zero");

        let mut workers = Vec::with_capacity(size);
        let mut senders = Vec::with_capacity(size);

        for id in 0..size {
            let (sender, receiver) = mpsc::channel();
            let receiver = Arc::new(Mutex::new(receiver));
            workers.push(Worker::new(id, Arc::clone(&receiver)));
            senders.push(sender);
        }

        ThreadPool {
            workers,
            senders,
            next: Mutex::new(0),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        let mut next = self.next.lock().unwrap();
        let sender = &self.senders[*next];
        *next = (*next + 1) % self.senders.len();
        sender.send(job).expect("Failed to send job to worker");
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        // Signal shutdown by clearing senders.
        self.senders.clear();
        println!("Shutting down.");

        // Join each worker.
        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);
            worker.thread.join().unwrap();
        }
    }
}

pub struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || loop {
            let message = receiver.lock().unwrap().recv();
            match message {
                Ok(job) => {
                    println!("Worker {id} got a job; executing.");
                    job();
                }
                Err(_) => {
                    println!("Worker {id} disconnected; shutting down.");
                    break;
                }
            }
        });
        Worker { id, thread }
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<String> = buf_reader
        .lines()
        .map(|result| result.unwrap_or_default())
        .take_while(|line| !line.is_empty())
        .collect();

    if http_request.is_empty() {
        let response = "HTTP/1.1 400 BAD REQUEST\r\nContent-Length: 0\r\n\r\n";
        stream.write_all(response.as_bytes()).unwrap();
        return;
    }
    let request_line = &http_request[0];
    let base_path = env!("CARGO_MANIFEST_DIR");
    let (status_line, filename) = match request_line.as_str() {
        "GET / HTTP/1.1" => (
            "HTTP/1.1 200 OK",
            format!("{}/src/hello.html", base_path)
        ),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            (
                "HTTP/1.1 200 OK",
                format!("{}/src/hello.html", base_path)
            )
        },
        "GET /unknown HTTP/1.1" => (
            "HTTP/1.1 404 NOT FOUND",
            format!("{}/src/404.html", base_path)
        ),
        _ => (
            "HTTP/1.1 404 NOT FOUND",
            format!("{}/src/404.html", base_path)
        ),
    };

    

    let contents = fs::read_to_string(filename)
        .unwrap_or_else(|_| String::from("File not found"));
    let length = contents.len();
    let response = format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");
    stream.write_all(response.as_bytes()).expect("Failed to write response");
}

fn main() {
    let listener = TcpListener::bind("127.0.0.1:8080")
        .expect("Failed to bind address. Is the port already in use?");
    listener.set_nonblocking(true).expect("Cannot set non-blocking");

    println!("Server running on 127.0.0.1:8080");
    let pool = ThreadPool::new(4);
    let running = Arc::new(AtomicBool::new(true));
    let running_clone = Arc::clone(&running);

    ctrlc::set_handler(move || {
        println!("\nCtrl+C pressed. Initiating shutdown...");
        running_clone.store(false, Ordering::SeqCst);
    })
    .expect("Error setting Ctrl+C handler");

    while running.load(Ordering::SeqCst) {
        match listener.accept() {
            Ok((stream, _addr)) => {
                
                pool.execute(move || {
                    handle_connection(stream);
                });
            }
            Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                thread::sleep(Duration::from_millis(100));
            }
            Err(e) => eprintln!("Error accepting connection: {}", e),
        }
    }

    // The pool is dropped here when main exits the loop.
    println!("Server shutting down gracefully.");
    // Optionally, you could force exit with:
    // std::process::exit(0);
}

use std::{
    sync::{mpsc, Arc, Mutex},
    thread,
};

pub type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<Worker>,
    // Use a Vec to store senders.
    senders: Vec<mpsc::Sender<Job>>,
    next: Mutex<usize>,
}

impl ThreadPool {
    
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0, "ThreadPool size must be greater than zero");

        let mut workers = Vec::with_capacity(size);
        let mut senders = Vec::with_capacity(size);

        // Create each worker with its own channel.
        for id in 0..size {
            let (sender, receiver) = mpsc::channel();
            // Wrap the receiver in an Arc and Mutex so it can be shared safely.
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

        // Get the next sender based on a round-robin index.
        let mut next = self.next.lock().unwrap();
        let sender = &self.senders[*next];
        *next = (*next + 1) % self.senders.len();

        sender.send(job).expect("Failed to send job to worker");
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        // Drop all senders so that each worker's receiver gets an error.
        self.senders.clear();

        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);
            // Join each worker thread.
            worker.thread.join().unwrap();
        }
    }
}

pub struct Worker {
    // The worker id helps us identify which worker handles the job.
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || loop {
            // Lock the receiver and block on recv.
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

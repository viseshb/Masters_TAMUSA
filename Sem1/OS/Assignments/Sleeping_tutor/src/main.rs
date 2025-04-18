use std::sync::mpsc::{self, SyncSender, TrySendError, Receiver};
use std::thread;
use std::time::Duration;
use rand::Rng;
use std::sync::{Arc, Mutex};
fn main() {
    let (tutor_sender, tutor_receiver) = mpsc::sync_channel(3);

    let students_helped = Arc::new(Mutex::new(0));
    let students_helped_tutor = Arc::clone(&students_helped);

    let tutor_handle = thread::spawn(move || {
        tutor(tutor_receiver, students_helped_tutor);
    });

    let mut student_handles = vec![];
    for id in 0..10 {
        let sender = tutor_sender.clone();
        let students_helped_student = Arc::clone(&students_helped);
        let handle = thread::spawn(move || {
            student(id, sender, students_helped_student);
        });
        student_handles.push(handle);
    }

    for handle in student_handles {
        handle.join().unwrap();
    }

    drop(tutor_sender);

    tutor_handle.join().unwrap();

    println!("All students have been helped at least once. Exiting.");
}

fn tutor(receiver: Receiver<(usize, SyncSender<()>)>, students_helped: Arc<Mutex<usize>>) {
    println!("Tutor started office hours.");
    loop {
        println!("Tutor is napping.");
        match receiver.recv() {
            Ok((student_id, response_sender)) => {
                println!("Tutor woke up to help student {}.", student_id);
                thread::sleep(Duration::from_secs(1));
                response_sender.send(()).expect("Failed to notify student");
                println!("Tutor finished helping student {}.", student_id);

                let mut helped = students_helped.lock().unwrap();
                *helped += 1;
            },
            Err(_) => {
                println!("Tutor office hours ended.");
                break;
            }
        }
    }
}

fn student(id: usize, sender: SyncSender<(usize, SyncSender<()>)>, students_helped: Arc<Mutex<usize>>) {
    let mut rng = rand::thread_rng();
    loop {
        println!("Student {} is studying.", id);
        let study_time = rng.gen_range(1..5);
        thread::sleep(Duration::from_secs(study_time));

        let helped = students_helped.lock().unwrap();
        if *helped >= 10 {
            drop(helped);
            break;
        }
        drop(helped);

        let (response_sender, response_receiver) = mpsc::sync_channel(0);
        match sender.try_send((id, response_sender)) {
            Ok(()) => {
                println!("Student {} is waiting in a chair.", id);
                response_receiver.recv().expect("Failed to receive help");
                println!("Student {} has been helped.", id);
            },
            Err(TrySendError::Full(_)) => {
                println!("Student {} found no chairs and will return later.", id);
            },
            Err(TrySendError::Disconnected(_)) => {
                break;
            }
        }
    }
}
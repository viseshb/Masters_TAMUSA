use std::sync::{Arc, Mutex, Condvar};
use std::thread;
use std::time::Duration;
use std::collections::VecDeque;
use rand::Rng;
use std::sync::atomic::{AtomicIsize, Ordering};

const NUM_STUDENTS: isize = 10;
const NUM_CHAIRS: usize = 3;
const HELP_REQUESTS: usize = 3;

struct TutorOffice {
    waiting_students: VecDeque<usize>,
    tutor_sleeping: bool,
    active_students: AtomicIsize,
    tutor_done: bool,
}

fn main() {
    let office = Arc::new((Mutex::new(TutorOffice {
        waiting_students: VecDeque::new(),
        tutor_sleeping: true,
        active_students: AtomicIsize::new(NUM_STUDENTS),
        tutor_done: false,
    }), Condvar::new()));

    let tutor_office = Arc::clone(&office);
    let tutor_thread = thread::spawn(move || {
        tutor(tutor_office);
    });

    let mut student_threads = vec![];
    for student_id in 0..NUM_STUDENTS as usize {
        let student_office = Arc::clone(&office);
        student_threads.push(thread::spawn(move || {
            student(student_id, student_office);
        }));
    }

    for t in student_threads {
        let _ = t.join();
    }

    {
        let (lock, condvar) = &*office;
        let mut office = lock.lock().unwrap_or_else(|e| e.into_inner());
        office.tutor_done = true;
        condvar.notify_all();
    }

    let _ = tutor_thread.join();
    println!("\n✅ All students have finished, and the tutor has left.");
}

fn tutor(office: Arc<(Mutex<TutorOffice>, Condvar)>) {
    let (lock, condvar) = &*office;

    loop {
        let mut office = lock.lock().unwrap_or_else(|e| e.into_inner());

        if office.active_students.load(Ordering::SeqCst) <= 0 {
            println!("\n[Tutor] No more students left. Exiting...\n");
            office.tutor_done = true;
            condvar.notify_all();
            return;
        }

        while office.waiting_students.is_empty() && !office.tutor_done {
            println!("[Tutor] No students, taking a nap...");
            office.tutor_sleeping = true;
            office = condvar.wait(office).unwrap_or_else(|e| e.into_inner());
        }

        if office.tutor_done {
            return;
        }

        if let Some(student_id) = office.waiting_students.pop_front() {
            let remaining = office.active_students.load(Ordering::SeqCst);
            println!("[Tutor] Helping student {} | Students still needing help: {}", student_id, remaining);

            office.tutor_sleeping = false;

            // Unlock the mutex before sleeping to avoid blocking other threads
            drop(office);
            thread::sleep(Duration::from_secs(2));

            // Re-lock and decrement active students count safely
            let office = lock.lock().unwrap_or_else(|e| e.into_inner());
            let new_remaining = office.active_students.fetch_sub(1, Ordering::SeqCst) - 1;
            println!("[Tutor] Finished helping student {} | Students still needing help: {}", student_id, new_remaining.max(0));
        }
    }
}

fn student(student_id: usize, office: Arc<(Mutex<TutorOffice>, Condvar)>) {
    let (lock, condvar) = &*office;
    let mut rng = rand::thread_rng();
    let mut help_count = 0;

    while help_count < HELP_REQUESTS {
        let study_time: u64 = rng.gen_range(1..=5) as u64;
        println!("[Student {}] Studying for {} seconds", student_id, study_time);
        thread::sleep(Duration::from_secs(study_time));

        let mut office = lock.lock().unwrap_or_else(|e| e.into_inner());
        if office.tutor_done {
            println!("[Student {}] Tutor is done. Exiting...", student_id);
            return;
        }

        if office.waiting_students.len() < NUM_CHAIRS {
            let remaining = office.active_students.load(Ordering::SeqCst);
            println!("[Student {}] Waiting in the hallway | Students still needing help: {}", student_id, remaining.max(0));
            office.waiting_students.push_back(student_id);
            condvar.notify_one();
        } else {
            println!("[Student {}] No chairs available, coming back later", student_id);
        }

        drop(office);
        thread::sleep(Duration::from_secs(2));
        help_count += 1;
    }

    let mut office = lock.lock().unwrap_or_else(|e| e.into_inner());
    let remaining = office.active_students.load(Ordering::SeqCst);
    if remaining > 0 {
       let new_remaining = office.active_students.fetch_sub(1, Ordering::SeqCst) - 1;
    if new_remaining == 0 {
        println!("[Student {}] Got all the help needed and is the last student. Ensuring tutor exits...", student_id);
        office.tutor_done = true;
        condvar.notify_all();
    } else {
        println!("[Student {}] Got all the help needed and is leaving. {} student(s) still need help.", student_id, new_remaining);
    }
}
}


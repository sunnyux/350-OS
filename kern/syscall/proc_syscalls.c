#include <types.h>
#include <kern/errno.h>
#include <kern/unistd.h>
#include <kern/wait.h>
#include <lib.h>
#include <syscall.h>
#include <current.h>
#include <proc.h>
#include <thread.h>
#include <addrspace.h>
#include <copyinout.h>

#include <mips/trapframe.h>
#include <synch.h>
#include <vm.h>
#include <vfs.h>

#include "opt-A2.h"

  /* this implementation of sys__exit does not do anything with the exit code */
  /* this needs to be fixed to get exit() and waitpid() working properly */

void sys__exit(int exitcode) {

  struct addrspace *as;
  struct proc *p = curproc;
  /* for now, just include this to keep the compiler from complaining about
     an unused variable */
  (void)exitcode;

  DEBUG(DB_SYSCALL,"Syscall: _exit(%d)\n",exitcode);

  KASSERT(curproc->p_addrspace != NULL);
  as_deactivate();
  /*
   * clear p_addrspace before calling as_destroy. Otherwise if
   * as_destroy sleeps (which is quite possible) when we
   * come back we'll be calling as_activate on a
   * half-destroyed address space. This tends to be
   * messily fatal.
   */
  as = curproc_setas(NULL);
  as_destroy(as);

  /* detach this thread from its process */
  /* note: curproc cannot be used after this call */
  proc_remthread(curthread);

#if OPT_A2
  // If parent has already exited or if already called waitpid (autopsy done)
  if (p->p_parent == NULL || !check_p_alive(p->p_parent)) {
    // children should delete themselves since they won't have a parent, 
    // zombies only when parent alive
    proc_destroy(p); 
  } else {
    lock_acquire(p->p_lk);
    p->p_alive = false;
    p->p_exit_code = exitcode;
    cv_signal(p->p_cv, p->p_parent->p_lk);
    lock_release(p->p_lk);
  }
#else
  /* if this is the last user process in the system, proc_destroy()
     will wake up the kernel menu thread */
  proc_destroy(p);
  
#endif
  thread_exit();
  /* thread_exit() does not return, so we should never get here */
  panic("return from thread_exit in sys_exit\n");
}


/* stub handler for getpid() system call                */
int
sys_getpid(pid_t *retval)
{
#if OPT_A2
  spinlock_acquire(&curproc->p_lock);
  *retval = curproc->p_pid;
  spinlock_release(&curproc->p_lock);
  return(0);

#else
  /* for now, this is just a stub that always returns a PID of 1 */
  /* you need to fix this to make it work properly */
  *retval = 1;
  return(0);
#endif
}

/* stub handler for waitpid() system call                */

int
sys_waitpid(pid_t pid,
        userptr_t status,
        int options,
        pid_t *retval)
{
  int exitstatus;
  int result;

  if (options != 0) {
    return(EINVAL);
  }

#if OPT_A2
  // Validate tht the given pid is from children
  bool is_child = false;
  struct proc *parent = curproc;
  lock_acquire(parent->p_lk);
  for (unsigned int i = 0; i < array_num(parent->p_children); i++) {
    struct proc *child = array_get(parent->p_children, i);
    if (child->p_pid == pid) {
      is_child = true;
      while(check_p_alive(child)) {
        cv_wait(child->p_cv, parent->p_lk); //
      }
      exitstatus = _MKWAIT_EXIT(child->p_exit_code);
      break;
    }
  }
  lock_release(parent->p_lk);
  if (!is_child) {
    *retval = -1;
    return ESRCH;
  }

#else
  /* this is just a stub implementation that always reports an
     exit status of 0, regardless of the actual exit status of
     the specified process.   
     In fact, this will return 0 even if the specified process
     is still running, and even if it never existed in the first place.

     Fix this!
  */

  /* for now, just pretend the exitstatus is 0 */
  exitstatus = 0;

#endif
  result = copyout((void *)&exitstatus,status,sizeof(int));
  if (result) {
    return(result);
  }
  *retval = pid;
  return(0);
}


// #if OPT_A2

int
sys_fork(struct trapframe* tf, 
         pid_t* retval)
{
  int err;
  struct proc *parent = curproc;
  struct proc *child;

  // create process structure for child process
  child = proc_create_runprogram(parent->p_name);
  if (child == NULL) {
    return ENOMEM;
  }

  // create and copy the address space
  spinlock_acquire(&parent->p_lock);
  err = as_copy(parent->p_addrspace, &child->p_addrspace);
  spinlock_release(&parent->p_lock);
  
  if (err != 0) {
    proc_destroy(child);
    return err;
  }

  // create parent/child relationship
  spinlock_acquire(&parent->p_lock);
  child->p_parent = parent;
  err = array_add(parent->p_children, (void *) child, NULL);
  spinlock_release(&parent->p_lock);

  if (err != 0) {
    proc_destroy(child);
    return err; 
  }

  // create a thread for the child process
  struct trapframe *tf_p = kmalloc(sizeof(struct trapframe));
  if (tf_p == NULL || tf == NULL) {
    proc_destroy(child);
    return ENOMEM;
  }

  spinlock_acquire(&parent->p_lock);
  memcpy(tf_p, tf, sizeof(struct trapframe));
  spinlock_release(&parent->p_lock);

  err = thread_fork(child->p_name, child, enter_forked_process, (void *)tf_p, 0);
  if (err != 0) {
    proc_destroy(child);
    return err;
  }

  // return
  *retval = child->p_pid;
  return 0;
}

// #endif

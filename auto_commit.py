#!/usr/bin/env python3
# Auto-commit script for git repositories
# Monitors directory changes and auto-commits them
"""
Auto-commit file watcher for git repositories.
Monitors the current directory for changes and automatically commits and pushes them.
"""

import os
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class GitAutoCommitHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.last_commit_time = 0
        self.debounce_delay = 2  # seconds to wait before committing after last change

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Ignore .git directory and common temporary/build files
        ignored_paths = ['.git', '__pycache__', '.pyc', 'dist', '*.egg-info', '.devin', 'venv']
        if any(ignored in event.src_path for ignored in ignored_paths):
            return
        
        print(f"Change detected: {event.src_path}")
        sys.stdout.flush()
        self.schedule_commit()

    def on_created(self, event):
        if event.is_directory:
            return
        
        # Ignore .git directory and common temporary/build files
        ignored_paths = ['.git', '__pycache__', '.pyc', 'dist', '*.egg-info', '.devin', 'venv']
        if any(ignored in event.src_path for ignored in ignored_paths):
            return
        
        print(f"File created: {event.src_path}")
        sys.stdout.flush()
        self.schedule_commit()

    def on_deleted(self, event):
        if event.is_directory:
            return
        
        # Ignore .git directory and common temporary/build files
        ignored_paths = ['.git', '__pycache__', '.pyc', 'dist', '*.egg-info', '.devin', 'venv']
        if any(ignored in event.src_path for ignored in ignored_paths):
            return
        
        print(f"File deleted: {event.src_path}")
        sys.stdout.flush()
        self.schedule_commit()

    def schedule_commit(self):
        """Schedule a commit after a debounce delay"""
        self.last_commit_time = time.time()
        # Wait for debounce delay before committing
        time.sleep(self.debounce_delay)
        
        # Check if there were more recent changes
        if time.time() - self.last_commit_time >= self.debounce_delay:
            self.commit_and_push()

    def commit_and_push(self):
        """Commit and push changes to git"""
        try:
            os.chdir(self.repo_path)
            
            # Check if there are changes to commit
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                print("No changes to commit")
                sys.stdout.flush()
                return
            
            print("Committing and pushing changes...")
            sys.stdout.flush()
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit with standard message
            subprocess.run(
                ['git', 'commit', '-m', 'Auto-commit: Project changes detected'],
                check=True
            )
            
            # Push to remote
            subprocess.run(['git', 'push'], check=True)
            
            print("Changes committed and pushed successfully!")
            sys.stdout.flush()
            
        except subprocess.CalledProcessError as e:
            print(f"Error during git operation: {e}")
            sys.stdout.flush()
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.stdout.flush()


def main():
    """Main function to start the file watcher"""
    repo_path = os.getcwd()
    print(f"Monitoring {repo_path} for changes...")
    sys.stdout.flush()
    print("Press Ctrl+C to stop the monitor")
    sys.stdout.flush()
    
    event_handler = GitAutoCommitHandler(repo_path)
    observer = Observer()
    observer.schedule(event_handler, repo_path, recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watcher...")
        sys.stdout.flush()
        observer.stop()
    
    observer.join()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
INTVL FAQ Search Launcher
Run this script from the project root to start the FAQ system.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("INTL FAQ Search System")
    print("=" * 40)
    print("1. Build embeddings")
    print("2. Start Q&A system")
    print("3. Test thresholds")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nChoose an option (1-4): ").strip()
            
            if choice == "1":
                print("\nBuilding embeddings...")
                from build_embeddings import build_embeddings
                build_embeddings()
                
            elif choice == "2":
                print("\nStarting Q&A system...")
                print("Type 'quit' to exit the Q&A system")
                from answer_questions import main as qa_main
                qa_main()
                
            elif choice == "3":
                print("\nTesting thresholds...")
                from test_threshold import test_thresholds
                test_thresholds()
                
            elif choice == "4":
                print("Quit!")
                break
                
            else:
                print("Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure you've run option 1 first to build the embeddings.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simple Test Sequence Script for Concierge Sales Assistant

This script automatically runs the first followup sequence (Product Analysis Flow)
to test context management with comprehensive timing analysis.
"""

import time
import sys
from datetime import datetime

# Import the concierge agent and test data
from concierge_sales_assistant import concierge_sales_agent, agent_execution_times
from benchmark.test_followup_questions_context_management import sequence_1_questions

def run_question(question: str, question_number: int):
    """Run a single question and show timing results"""
    print(f"\n{'='*70}")
    print(f"🧪 Question {question_number}/8")
    print(f"❓ {question}")
    print(f"{'='*70}")
    
    # Reset agent execution times
    agent_execution_times.clear()
    
    # Start timing
    start_time = time.time()
    print(f"⏱️  [TIMING] Starting query execution...")
    print()
    
    try:
        # Execute the query
        print("🤖 ConciergeBot: ", end="")
        response = concierge_sales_agent(question)
        
        # End timing
        end_time = time.time()
        total_time = end_time - start_time
        
        # Print timing summary
        print()
        print("=" * 60)
        print("⏱️  [TIMING SUMMARY]")
        print("=" * 60)
        
        if agent_execution_times:
            for agent_name, execution_time in agent_execution_times.items():
                print(f"   📊 {agent_name.capitalize()} Agent: {execution_time:.2f} seconds")
            print("   " + "-" * 40)
            sub_agent_total = sum(agent_execution_times.values())
            print(f"   📊 Sub-agents Total: {sub_agent_total:.2f} seconds")
            coordinator_time = total_time - sub_agent_total
            print(f"   🤖 Coordinator Overhead: {coordinator_time:.2f} seconds")
        else:
            print("   📊 No sub-agents were called for this query")
        
        print(f"   ⏱️  Total Query Time: {total_time:.2f} seconds")
        print("=" * 60)
        
        return total_time, True
        
    except Exception as e:
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\n❌ ERROR: {str(e)}")
        print(f"⏱️  Query failed after {total_time:.2f} seconds")
        return total_time, False

def main():
    """Run the first followup sequence (Product Analysis Flow)"""
    print("🏢 CONCIERGE SALES ASSISTANT - PRODUCT ANALYSIS SEQUENCE TEST")
    print("=" * 80)
    print("📊 This will run the Product Analysis Flow sequence (8 questions)")
    print("🔄 Testing context management and timing performance")
    print()
    
    # Ask for confirmation
    try:
        confirm = input("Do you want to proceed with the test sequence? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Test cancelled.")
            return
    except KeyboardInterrupt:
        print("\nTest cancelled.")
        return
    
    # Start the sequence
    start_time = time.time()
    print(f"\n🚀 Starting Product Analysis Flow Sequence")
    print(f"⏰ Start Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📝 Total Questions: {len(sequence_1_questions)}")
    
    successful_questions = 0
    total_query_time = 0
    
    try:
        for i, question in enumerate(sequence_1_questions, 1):
            query_time, success = run_question(question, i)
            total_query_time += query_time
            if success:
                successful_questions += 1
            
            # Brief pause between questions (except for last question)
            if i < len(sequence_1_questions):
                print(f"\n⏸️  Pausing 2 seconds before next question...")
                time.sleep(2)
        
        # Final summary
        end_time = time.time()
        total_duration = end_time - start_time
        
        print(f"\n🎉 SEQUENCE COMPLETE!")
        print("=" * 70)
        print(f"⏰ Total Duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
        print(f"⏱️  Total Query Time: {total_query_time:.2f} seconds")
        print(f"🕒 Overhead Time: {(total_duration - total_query_time):.2f} seconds")
        print(f"📊 Questions Completed: {successful_questions}/{len(sequence_1_questions)}")
        print(f"📈 Success Rate: {(successful_questions/len(sequence_1_questions)*100):.1f}%")
        print(f"📊 Average Query Time: {(total_query_time/len(sequence_1_questions)):.2f} seconds")
        print(f"🏁 End Time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Test sequence interrupted by user")
        print(f"✅ Completed {successful_questions}/{len(sequence_1_questions)} questions")
    except Exception as e:
        print(f"\n❌ Test sequence failed: {str(e)}")
        print(f"✅ Completed {successful_questions}/{len(sequence_1_questions)} questions")

if __name__ == "__main__":
    main()
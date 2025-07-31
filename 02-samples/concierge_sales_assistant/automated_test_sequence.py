#!/usr/bin/env python3
"""
Automated Test Sequence Script for Concierge Sales Assistant

This script automatically runs all benchmark questions and followup sequences
to test the concierge sales assistant with comprehensive timing analysis.
"""

import time
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Import the concierge agent and test data
from concierge_sales_assistant import concierge_sales_agent, agent_execution_times
from benchmark.all_questions import qs_concierge_benchmark
from benchmark.test_followup_questions_context_management import all_followup_test_sequences

class TestSequenceRunner:
    def __init__(self):
        self.results = []
        self.total_start_time = None
        self.total_end_time = None
        
    def run_single_question(self, question: str, sequence_name: str = "single", question_number: int = 1) -> Dict[str, Any]:
        """Run a single question and collect timing/response data"""
        print(f"\n{'='*80}")
        print(f"🧪 TESTING: {sequence_name} - Question {question_number}")
        print(f"❓ QUESTION: {question}")
        print(f"{'='*80}")
        
        # Reset agent execution times
        agent_execution_times.clear()
        
        # Start timing
        start_time = time.time()
        
        try:
            # Execute the query
            response = concierge_sales_agent(question)
            
            # End timing
            end_time = time.time()
            total_time = end_time - start_time
            
            # Collect results
            result = {
                'sequence_name': sequence_name,
                'question_number': question_number,
                'question': question,
                'total_time': total_time,
                'agent_times': dict(agent_execution_times),
                'sub_agent_total': sum(agent_execution_times.values()) if agent_execution_times else 0,
                'coordinator_overhead': total_time - sum(agent_execution_times.values()) if agent_execution_times else total_time,
                'agents_used': list(agent_execution_times.keys()) if agent_execution_times else [],
                'response_length': len(str(response)) if response else 0,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            # Print timing summary
            self._print_timing_summary(result)
            
            return result
            
        except Exception as e:
            end_time = time.time()
            total_time = end_time - start_time
            
            result = {
                'sequence_name': sequence_name,
                'question_number': question_number,
                'question': question,
                'total_time': total_time,
                'agent_times': {},
                'sub_agent_total': 0,
                'coordinator_overhead': total_time,
                'agents_used': [],
                'response_length': 0,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"❌ ERROR: {str(e)}")
            return result
    
    def _print_timing_summary(self, result: Dict[str, Any]):
        """Print timing summary for a single question"""
        print(f"\n⏱️  [TIMING SUMMARY]")
        print(f"{'='*60}")
        
        if result['agent_times']:
            for agent_name, execution_time in result['agent_times'].items():
                print(f"   📊 {agent_name.capitalize()} Agent: {execution_time:.2f}s")
            print(f"   {'-'*40}")
            print(f"   📊 Sub-agents Total: {result['sub_agent_total']:.2f}s")
            print(f"   🤖 Coordinator Overhead: {result['coordinator_overhead']:.2f}s")
        else:
            print(f"   📊 No sub-agents called")
        
        print(f"   ⏱️  Total Query Time: {result['total_time']:.2f}s")
        print(f"   📝 Response Length: {result['response_length']} chars")
        print(f"   🎯 Agents Used: {', '.join(result['agents_used']) if result['agents_used'] else 'None'}")
        print(f"{'='*60}")
    
    def run_followup_sequences(self):
        """Run the followup question sequences that test context management"""
        print(f"\n🔄 STARTING FOLLOWUP SEQUENCES TEST")
        print(f"{'='*80}")
        
        for sequence_name, questions in all_followup_test_sequences.items():
            print(f"\n🎯 Starting Sequence: {sequence_name}")
            print(f"📝 Questions in sequence: {len(questions)}")
            
            for i, question in enumerate(questions, 1):
                result = self.run_single_question(question, sequence_name, i)
                self.results.append(result)
                
                # Brief pause between questions in sequence
                time.sleep(1)
            
            print(f"\n✅ Completed Sequence: {sequence_name}")
            print(f"⏸️  Pausing 3 seconds before next sequence...")
            time.sleep(3)
    
    def run_benchmark_questions(self):
        """Run all benchmark questions"""
        print(f"\n🧪 STARTING BENCHMARK QUESTIONS TEST")
        print(f"{'='*80}")
        print(f"📝 Total benchmark questions: {len(qs_concierge_benchmark)}")
        
        for i, question in enumerate(qs_concierge_benchmark, 1):
            result = self.run_single_question(question, "benchmark", i)
            self.results.append(result)
            
            # Brief pause between questions
            time.sleep(1)
        
        print(f"\n✅ Completed all benchmark questions")
    
    def run_all_tests(self):
        """Run all test sequences"""
        self.total_start_time = time.time()
        
        print(f"\n🚀 STARTING AUTOMATED TEST SEQUENCE")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        try:
            # Run followup sequences first (context management)
            self.run_followup_sequences()
            
            # Run benchmark questions
            self.run_benchmark_questions()
            
            self.total_end_time = time.time()
            self._print_final_summary()
            
        except KeyboardInterrupt:
            print(f"\n⚠️  Test sequence interrupted by user")
            self.total_end_time = time.time()
            self._print_final_summary()
        except Exception as e:
            print(f"\n❌ Test sequence failed: {str(e)}")
            self.total_end_time = time.time()
            self._print_final_summary()
    
    def _print_final_summary(self):
        """Print comprehensive test summary"""
        total_duration = self.total_end_time - self.total_start_time if self.total_end_time and self.total_start_time else 0
        successful_tests = len([r for r in self.results if r['success']])
        failed_tests = len([r for r in self.results if not r['success']])
        
        print(f"\n🎉 FINAL TEST SUMMARY")
        print(f"{'='*80}")
        print(f"⏰ Total Duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
        print(f"📊 Total Questions: {len(self.results)}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(successful_tests/len(self.results)*100):.1f}%" if self.results else "0%")
        
        if self.results:
            # Timing statistics
            successful_results = [r for r in self.results if r['success']]
            if successful_results:
                avg_time = sum(r['total_time'] for r in successful_results) / len(successful_results)
                min_time = min(r['total_time'] for r in successful_results)
                max_time = max(r['total_time'] for r in successful_results)
                
                print(f"\n⏱️  TIMING STATISTICS:")
                print(f"   📊 Average Query Time: {avg_time:.2f}s")
                print(f"   🏃 Fastest Query: {min_time:.2f}s")
                print(f"   🐌 Slowest Query: {max_time:.2f}s")
            
            # Agent usage statistics
            agent_usage = {}
            for result in successful_results:
                for agent in result['agents_used']:
                    agent_usage[agent] = agent_usage.get(agent, 0) + 1
            
            if agent_usage:
                print(f"\n🤖 AGENT USAGE STATISTICS:")
                for agent, count in sorted(agent_usage.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / successful_tests * 100) if successful_tests > 0 else 0
                    print(f"   📊 {agent.capitalize()}: {count} times ({percentage:.1f}%)")
        
        # Failed tests summary
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.results:
                if not result['success']:
                    print(f"   • {result['sequence_name']} Q{result['question_number']}: {result.get('error', 'Unknown error')}")
        
        print(f"\n📝 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

def main():
    """Main function to run the automated test sequence"""
    print("🏢 CONCIERGE SALES ASSISTANT - AUTOMATED TEST SEQUENCE")
    print("=" * 80)
    print("This script will automatically run all benchmark questions and followup sequences.")
    print("Each question will be timed and analyzed for performance.")
    print()
    
    # Ask for confirmation
    try:
        confirm = input("Do you want to proceed with the automated test? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Test cancelled.")
            return
    except KeyboardInterrupt:
        print("\nTest cancelled.")
        return
    
    # Run the tests
    runner = TestSequenceRunner()
    runner.run_all_tests()
    
    print("\n🎯 Test sequence complete!")
    print("💡 You can now analyze the performance data and identify any issues.")

if __name__ == "__main__":
    main()
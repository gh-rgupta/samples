# Follow-up Questions for Context Management Testing
# Tests the assistant's ability to maintain context across a conversation sequence

# Sequence 1: Product Information and Order Analysis
sequence_1_questions = [
    "Tell me few features of Guardant360",
    "Can you give some information on Guardant Reveal",
    "Can you compare above two tests",
    "Can you add tissue to that comparison",
    "What is standard turnaround time for above tests",
    "What is standard turnaround time for these tests",
    "How much such tests Dr. Shafique ordered",
    "Which account has more than 2 such orders cancelled last quarter",
    "Show me test ordering trend of these tests"
]

# Sequence 2: Physician Engagement and Analysis
sequence_2_questions = [
    "Who had last engagement with Dr. Julie",
    "What are main talking points in these engagement",
    "What was the main outcome of that engagement",
    "Do you have any recommendations to make these engagements better",
    "What tests were ordered by this doctor last month",
    "Have I reached Stark limit for this physician"
]

# Combined test sequences
all_followup_test_sequences = {
    "product_analysis_sequence": sequence_1_questions,
    "physician_engagement_sequence": sequence_2_questions
}

if __name__ == "__main__":
    print("=== Context Management Test Questions ===")
    print("\n📊 Sequence 1: Product Analysis Flow")
    for i, q in enumerate(sequence_1_questions, 1):
        print(f"{i}. {q}")
    
    print("\n👥 Sequence 2: Physician Engagement Flow")  
    for i, q in enumerate(sequence_2_questions, 1):
        print(f"{i}. {q}")
    
    print(f"\nTotal test sequences: {len(all_followup_test_sequences)}")
    print(f"Total questions: {len(sequence_1_questions) + len(sequence_2_questions)}")
 
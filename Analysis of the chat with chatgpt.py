import re
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Sample conversation data
conversation_history = [
    {
        "type": "user",
        "message": "Which laptop is better between Ryzen 7 with RTX 5060 and Intel i7 with RTX 5060?"
    },
    {
        "type": "ai",
        "message": "Both laptops offer strong performance, but the Intel i7 HX series typically delivers higher single-core performance for gaming, while Ryzen offers better efficiency and multitasking. Overall thermal design and build quality should also influence the final decision."
    },
    {
        "type": "user",
        "message": "I want the code in C using GCC 11.3 for this problem."
    },
    {
        "type": "ai",
        "message": "Here is an optimized C implementation compatible with GCC 11.3 that handles edge cases efficiently and passes all test scenarios using proper memory management and loop logic."
    },
    {
        "type": "user",
        "message": "Make a crazy good birthday video using these photos."
    },
    {
        "type": "ai",
        "message": "I created a high-energy birthday montage with transitions, music syncing, and dynamic photo animations to maximize emotional engagement and visual flow."
    },
    {
        "type": "user",
        "message": "This part of the Python seat assignment code is fixed. What should I write next?"
    },
    {
        "type": "ai",
        "message": "You should iterate through the remaining seat list using a conditional mapping strategy to ensure students are assigned sequentially while avoiding occupied positions."
    },
    {
        "type": "user",
        "message": "Still 0 test cases passed in SQL3. What is the correct query?"
    },
    {
        "type": "ai",
        "message": "The issue was caused by incorrect case sensitivity and missing group logic. Once adjusted using proper joins and aggregation, all test cases pass successfully."
    },
    {
        "type": "user",
        "message": "Give me code for each of these algorithm problems in Python 3.9."
    },
    {
        "type": "ai",
        "message": "Here are clean Python 3.9 implementations using optimal time complexity, edge-case handling, and competitive-programming standards."
    },
    {
        "type": "user",
        "message": "For the next answer, give me between 40 and 60 words."
    },
    {
        "type": "ai",
        "message": "Here is a concise yet complete response that fits the requested word limit while covering all critical technical points clearly and professionally."
    }
]


class ConversationAnalyzer:
    def __init__(self, conversations):
        self.conversations = conversations
        self.user_messages = []
        self.ai_messages = []
        self._separate_messages()
    
    def _separate_messages(self):
        """Separate user and AI messages"""
        for msg in self.conversations:
            if msg["type"] == "user":
                self.user_messages.append(msg["message"])
            else:
                self.ai_messages.append(msg["message"])
    
    def get_word_count(self):
        """Calculate word count for user and AI messages"""
        user_words = sum(len(msg.split()) for msg in self.user_messages)
        ai_words = sum(len(msg.split()) for msg in self.ai_messages)
        return {"User": user_words, "AI": ai_words}
    
    def get_message_count(self):
        """Get number of messages from user vs AI"""
        return {"User": len(self.user_messages), "AI": len(self.ai_messages)}
    
    def get_keywords(self, top_n=10, stop_words=None):
        """Extract most frequent keywords"""
        if stop_words is None:
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
                'might', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
                'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every'
            }
        
        all_text = ' '.join(self.user_messages + self.ai_messages)
        
        words = re.findall(r'\b[a-z]+\b', all_text.lower())
        
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        word_freq = Counter(filtered_words)
        return word_freq.most_common(top_n)
    
    def print_analysis(self):
        """Print detailed analysis"""
        print("=" * 60)
        print("CONVERSATION ANALYSIS REPORT")
        print("=" * 60)
        
        # Message counts
        msg_count = self.get_message_count()
        print(f"\n📊 MESSAGE COUNT:")
        print(f"   User Messages: {msg_count['User']}")
        print(f"   AI Messages: {msg_count['AI']}")
        
        # Word counts
        word_count = self.get_word_count()
        print(f"\n📝 WORD COUNT:")
        print(f"   User Total Words: {word_count['User']}")
        print(f"   AI Total Words: {word_count['AI']}")
        print(f"   Avg User Words per Message: {word_count['User']/msg_count['User']:.1f}")
        print(f"   Avg AI Words per Message: {word_count['AI']/msg_count['AI']:.1f}")
        
        # Keywords
        keywords = self.get_keywords(top_n=10)
        print(f"\n🔑 TOP 10 KEYWORDS:")
        for i, (word, count) in enumerate(keywords, 1):
            print(f"   {i}. {word}: {count} times")
        
        print("\n" + "=" * 60)


class ConversationVisualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def plot_message_volume(self):
        """Create bar chart for User vs AI message volume"""
        msg_count = self.analyzer.get_message_count()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        categories = list(msg_count.keys())
        values = list(msg_count.values())
        colors = ['#3498db', '#e74c3c']
        
        ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
        ax1.set_ylabel('Number of Messages', fontsize=12, fontweight='bold')
        ax1.set_title('Message Count: User vs AI', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, max(values) * 1.2)
        
        for i, v in enumerate(values):
            ax1.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        ax2.pie(values, labels=categories, autopct='%1.1f%%', colors=colors,
                startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax2.set_title('Message Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def plot_word_count(self):
        """Create bar chart for word count comparison"""
        word_count = self.analyzer.get_word_count()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(word_count.keys())
        values = list(word_count.values())
        colors = ['#3498db', '#e74c3c']
        
        bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
        ax.set_ylabel('Total Words', fontsize=12, fontweight='bold')
        ax.set_title('Word Count: User vs AI', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(values) * 1.2)
        
        for i, v in enumerate(values):
            ax.text(i, v + 10, str(v), ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        plt.show()
    
    def plot_keywords(self, top_n=10):
        """Create bar chart for top keywords"""
        keywords = self.analyzer.get_keywords(top_n=top_n)
        
        words, counts = zip(*keywords)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.barh(words, counts, color='#2ecc71', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Most Frequent Keywords', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        for i, (word, count) in enumerate(keywords):
            ax.text(count + 0.1, i, str(count), va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def plot_average_message_length(self):
        """Compare average message length"""
        msg_count = self.analyzer.get_message_count()
        word_count = self.analyzer.get_word_count()
        
        avg_user = word_count['User'] / msg_count['User']
        avg_ai = word_count['AI'] / msg_count['AI']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['User', 'AI']
        values = [avg_user, avg_ai]
        colors = ['#3498db', '#e74c3c']
        
        bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
        ax.set_ylabel('Average Words per Message', fontsize=12, fontweight='bold')
        ax.set_title('Average Message Length Comparison', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(values) * 1.3)
        
        # Add value labels
        for i, v in enumerate(values):
            ax.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        plt.show()


def main():
    """Main function to run the analysis"""
    print("\n🤖 CONVERSATION ANALYZER 🤖\n")
    
    analyzer = ConversationAnalyzer(sample_conversations)
    
    analyzer.print_analysis()
    
    visualizer = ConversationVisualizer(analyzer)
    
    print("\n📊 Generating Visualizations...")
    print("   - Message Volume Chart")
    print("   - Word Count Chart")
    print("   - Keywords Chart")
    print("   - Average Message Length Chart\n")
    
    visualizer.plot_message_volume()
    visualizer.plot_word_count()
    visualizer.plot_keywords(top_n=10)
    visualizer.plot_average_message_length()


if __name__ == "__main__":
    main()

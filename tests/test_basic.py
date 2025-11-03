import unittest
import json
from unittest.mock import patch, MagicMock

class TestStoryProcessing(unittest.TestCase):
    @patch('subprocess.run')
    def test_process_story(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Local Government')
        story = {'title': 'City Council Meeting', 'content': 'The city council met to discuss local issues.'}
        
        topic_list = ["Local Government", "Education", "Public Safety", "Other"]
        prompt = f"""
        Assign this news story to exactly ONE topic from the following list:
        {', '.join(topic_list)}

        Choose the topic that best represents what this story is primarily about.

        Title: {story['title']}
        Content: {story['content']}

        Return only the topic name from the list above.
        """
        
        # Simulate calling the llm command
        assigned_topic = mock_run(prompt)
        
        self.assertEqual(assigned_topic.stdout.strip(), 'Local Government')

if __name__ == '__main__':
    unittest.main()
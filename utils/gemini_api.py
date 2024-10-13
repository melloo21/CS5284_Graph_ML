import os
from dotenv import load_dotenv
import requests
import json
import google.generativeai as genai
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class GeminiAPI():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_AI_API_TRIAL')


        # Define the API endpoint
        self.url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
        genai.configure(api_key=self.api_key)

        
    
    def inference(self, text):

        # # Define the headers
        # headers = {
        #     'Content-Type': 'application/json',
        # }

        # # Define the data payload
        # data = {
        #     "contents": [
        #         {
        #             "parts": [
        #                 {
        #                     "text": "Summarise the following movie summary to less than 500 words: " + str(text)
        #                 }
        #             ]
        #         }
        #     ]
        # }

        # # Make the POST request
        # response = requests.post(f'{self.url}?key={self.api_key}', headers=headers, data=json.dumps(data))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content("Summarise the following movie summary to less than 500 words: " + str(text), 
                safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            })
        # print("Response:", response.text)
        # # Check the response status and content
        # if response.status_code == 200:
        #     res = response.json()
        #     print("Response:", res)
        # else:
        #     print("Failed to make the request. Status code:", response.status_code)
        #     print("Response:", response.text)
        # return response['candidates'][0]['content']['parts'][0]['text']
        return response.text

if __name__ == '__main__':
    gemini_api = GeminiAPI()
    input_text = """ A group of sentient toys, who pretend to be lifeless when humans are around, are preparing to move into a new house with their young owner Andy Davis, his infant sister Molly, and their single mother Mrs. Davis. Learning that Andy\'s birthday party has been unexpectedly moved to an earlier date, several toys — including Mr. Potato Head, Slinky Dog, Rex the tyrannosaur, Hamm the piggy bank, and Bo Peep the porcelain doll — become concerned that Andy might receive something that will replace them. To calm them, Sheriff Woody, Andy\'s favorite toy and their de facto leader, sends Sarge and his green army men to spy on Andy\'s birthday party with a baby monitor. Andy receives a Buzz Lightyear action figure, who believes he is an actual Space Ranger and does not know he is really a toy. Buzz impresses the others with his high-tech features and becomes Andy\'s new favorite toy, provoking Woody\'s jealousy.\nTwo days before the move, Andy\'s family plans for a dinner at Pizza Planet. To ensure Andy brings him along and not Buzz, Woody tries knocking Buzz behind the desk with RC, the radio-controlled car. However, Buzz is accidentally knocked out of the bedroom window instead, and most of the other toys believe Woody has deliberately killed Buzz. Andy takes Woody with him, but Buzz furiously confronts him in the car. The two fight, fall out of the car, and are left behind; after a further quarrel, they hitch a ride to the restaurant on a Pizza Planet delivery truck.\nAt Pizza Planet, Buzz mistakes a claw crane full of toy aliens for a rocket, and climbs in, pursued by Woody. Sid Phillips, Andy\'s sadistic next-door neighbor, takes the two from the crane to his house, where they encounter his Bull Terrier Scud and his "mutant" toys, made from parts of other toys he has destroyed.\nBuzz, after watching a television commercial promoting him, suffers an existential crisis, realizing he is a toy after all. He attempts to fly but falls and breaks his arm. After Sid\'s toys fix Buzz, Sid tapes Buzz to a firework rocket, planning to blow him up the following day. Overnight, Woody helps Buzz realize that his purpose is to make Andy happy, restoring Buzz\'s resolve. Sid takes Buzz out to blow him up, but Woody rallies the mutant toys to "break the rules" and frighten Sid into never harming toys again.\nNow freed, Woody and Buzz pursue the Davis\' moving truck, but Scud attacks Woody. Buzz stays behind to fight off the dog; Woody climbs into the truck, and pushes RC out to rescue Buzz. Still thinking Woody has killed another toy, the others also toss him out of the truck. Woody and Buzz pursue the truck on RC, and the other toys see them and realize their mistake. RC\'s batteries run out, forcing Woody to ignite the rocket strapped to Buzz. Buzz opens his wings to sever the tape just before the rocket explodes; he and Woody glide through the sunroof of Mrs. Davis\' car, landing safely inside.\nAs the toys listen in on the Christmas gift opening in the new house, Mr. Potato Head is delighted when Molly gets a Mrs. Potato Head. Woody and Buzz jokingly ponder what gift could be "worse" than Buzz, only to nervously smile at each other when Andy gets a dachshund puppy.
    """
    output = gemini_api.inference(input_text)
    if output:
        print("API Response:", output)
    else:
        print("Failed to get a valid response.")
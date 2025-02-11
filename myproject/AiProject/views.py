from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import google.generativeai as genai
import json
import re




# Configure Google Generative AI with API Key
genai.configure(api_key="AIzaSyAYspxEfFmhq0MT8lKeri7oF0Gmuxv27CU")

# User Registration API
@api_view(['POST'])
def register_user(request):
    """
    Register a new user with Full Name, Student ID, and Email.
    """
    if request.method == 'POST':
        # Deserialize the incoming data using UserSerializer
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user to the database
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def generate_mcqs(request):
    """
    Generate MCQs based on subject, difficulty, and number of questions.
    """
    subject = request.data.get("subject", "").strip()
    difficulty = request.data.get("difficulty", "").strip()
    num_questions = request.data.get("num_questions", 5)

    
    if not subject:
        return Response({"error": "Subject is required"}, status=400)
    if difficulty.lower() not in ["easy", "medium", "hard"]:
        return Response({"error": "Difficulty must be easy, medium, or hard"}, status=400)
    if not str(num_questions).isdigit() or int(num_questions) <= 0:
        return Response({"error": "Number of questions must be a positive integer"}, status=400)

    num_questions = int(num_questions)  

    
    prompt = f"""
    Generate {num_questions} multiple-choice questions on {subject} with a {difficulty} difficulty level.
    Each question should have 4 answer choices (A, B, C, D), and the correct answer should be clearly indicated.

    Return ONLY JSON format without explanations:
    {{
      "mcqs": [
        {{
          "question": "Sample question?",
          "options": {{
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
          }},
          "answer": "A"
        }},
        ...
      ]
    }}
    """

    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    raw_response = response.text.strip()

    
    match = re.search(r"\{.*\}", raw_response, re.DOTALL)
    if not match:
        return Response({"error": "Invalid AI response format"}, status=500)

    json_text = match.group(0)  

    try:
        mcqs_json = json.loads(json_text)  
        return Response(mcqs_json)
    except json.JSONDecodeError:
        return Response({"error": "Failed to parse AI response into JSON"}, status=500)



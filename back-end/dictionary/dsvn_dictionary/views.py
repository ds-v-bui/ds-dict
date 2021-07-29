import speech_recognition as sr
import pandas as pd
import os

from googletrans import Translator
from django import db
from django.db.models import query
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import serializers, status
from dsvn_dictionary.models import DsvnDictionary, User, Vi_Dictionary, Ja_Dictionary
from dsvn_dictionary.serializers import DsvnDictionarySerializer
from dsvn_dictionary.serializers import Vi_DictionarySerializer, Ja_DictionarySerializer, UserSerializer, UserLoginSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from dsvn_dictionary.variable_global import *
from django.db import connections

# class import excel file to database
@permission_classes([AllowAny])
class ImportExcelView(APIView):
    def post(self, request):
        df = pd.read_excel (FILE_NAME, sheet_name=SHEET_NAME).fillna('')
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
            query = """INSERT INTO {} (hiragana_text, kanji_text, katakana_text, vi_text, example, description, created_at, update_at) VALUES (%s, %s, %s, %s, %s, %s, now(), now())""".format(TABLE_NAME)
            hiragana_text, kanji_text, katakana_text, vi_text, example, description = '', '', '', '', '', ''
            for r in range(0, len(df)):
                hiragana_text = df.loc[r, 'hiragana_text']
                kanji_text = df.loc[r, 'kanji_text']
                katakana_text = df.loc[r, 'katakana_text']
                vi_text = df.loc[r, 'vi_text']
                example = df.loc[r, 'example']
                description = df.loc[r, 'description']

                # when vietnamese translate is null, skip row
                if vi_text == '':
                    continue
                # when column hiragana_text and katakana_text and kanji_text is null, skip row
                if hiragana_text == '' and katakana_text == '' and kanji_text == '':
                    continue
                
                values = (hiragana_text, kanji_text, katakana_text, vi_text, example, description)
                c.execute(query, values)
                
            c.close()
            db_conn.commit()
            db_conn.close()
        except:
            return JsonResponse({'message':'File excel is not imported'}, status=status.HTTP_400_BAD_REQUEST)    
        return JsonResponse({'message': 'File excel is import successfully!'}, status=status.HTTP_200_OK)

# class register user
@permission_classes([AllowAny])
class UserRegisterView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        email_register = request.data['email']
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return JsonResponse({
                'message': 'Email %r register successfully!' %email_register
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This email %r has already exist!' %email_register,
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)

# class check login
@permission_classes([AllowAny])
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)

# google speech voice vietnamese to text
@permission_classes([AllowAny])
class ViSpeechGooleView(APIView):
    def post(self, request):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Speak Anything :")
                audio = r.listen(source)
                text = ''
                try:
                    text = r.recognize_google(audio, language='vi-VN')
                    print("You said : {}".format(text))
                except:
                    JsonResponse({'message': "Sorry could not recognize what you said"}, status=status.HTTP_400_BAD_REQUEST)
                if text == '':
                    return JsonResponse({'message': "Sorry could not recognize what you said"}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': format(text)}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({'message': "The device not support the voice speak"}, status=status.HTTP_400_BAD_REQUEST)

# google speech voice japanese to text
@permission_classes([AllowAny])
class JaSpeechGooleView(APIView):
    def post(self, request):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Speak Anything :")
                audio = r.listen(source)
                text = ''
                try:
                    text = r.recognize_google(audio, language='ja-JA')
                    print("You said : {}".format(text))
                except:
                    JsonResponse({'message': "Sorry could not recognize what you said"}, status=status.HTTP_400_BAD_REQUEST)
                if text == '':
                    return JsonResponse({'message': "Sorry could not recognize what you said"}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': format(text)}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({'message': "The device not support the voice speak"}, status=status.HTTP_400_BAD_REQUEST)

# working list all in vidic
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE'])
def vidictionary_list(request):

    # function get all list of vi-dictionary
    if request.method == 'GET':
        tutorials = Vi_Dictionary.objects.all()
        
        vi_text = request.GET.get('vi_text', None)
        if vi_text is not None:
            tutorials = tutorials.filter(title__icontains=vi_text)
        
        tutorials_serializer = Vi_DictionarySerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
 
    # function add to vi-dictionary
    elif request.method == 'POST':
        vidic_data = JSONParser().parse(request)
        vidic_serializer = Vi_DictionarySerializer(data=vidic_data)
        if Vi_Dictionary.objects.filter(vi_text=vidic_serializer.initial_data['vi_text']).exists():
            return JsonResponse({'message': 'The vi_text to insert is exist in database'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if vidic_serializer.is_valid():
                vidic_serializer.save()
                return JsonResponse({'message': 'The vi_text insert successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(vidic_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    # function delete all list of vi-dictionary
    elif request.method == 'DELETE':
        count = Vi_Dictionary.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

# function search by vi to ja
@permission_classes([AllowAny])
@api_view(['GET', 'POST', 'DELETE'])
def vidictionary_search(request):
    if request.method == 'GET':
        title_name=request.GET['vi_text']

        tutorials = Vi_Dictionary.objects.raw("SELECT id, vi_text FROM dsvn_dictionary_vi_dictionary WHERE vi_text=%s",[title_name])
        tutorials_serializer = Vi_DictionarySerializer(tutorials, many=True)
        
        return JsonResponse(tutorials_serializer.data, safe=False)

# function update vi-dic by id
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def vidictionary_update(request, pk):

    try: 
        tutorial = Vi_Dictionary.objects.get(id=pk) 
    except Vi_Dictionary.DoesNotExist: 
        return JsonResponse({'message': 'The vi dictionary does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = Vi_DictionarySerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse({'message': 'The record was updated successfully!'}, status=status.HTTP_202_ACCEPTED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# function delete vi-dic by id
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE'])
def vidictionary_delete(request, pk):

    try: 
        vi_dic = Vi_Dictionary.objects.get(pk=pk) 
    except Vi_Dictionary.DoesNotExist: 
        return JsonResponse({'message': 'The vi dictionary does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'DELETE': 
        vi_dic.delete() 
        return JsonResponse({'message': 'The vi dictionary was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    

    # if request.method == 'DELETE':
    #     title_name = request.GET['vi_text']
    #     Vi_Dictionary.objects.filter(vi_text = title_name).delete()
    #     return JsonResponse({'message': 'Tutorials were deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# working list all in jadic
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE'])
def jadictionary_list(request):

    # function get all list of ja-dictionary
    if request.method == 'GET':
        ja_dic = Ja_Dictionary.objects.all()
        
        hiragana_text = request.GET.get('hiragana_text', None)
        if hiragana_text is not None:
            ja_dic = ja_dic.filter(title__icontains=hiragana_text)
        
        ja_serializer = Ja_DictionarySerializer(ja_dic, many=True)
        return JsonResponse(ja_serializer.data, safe=False)
 
    # function add to ja-dictionary
    elif request.method == 'POST':
        jadic_data = JSONParser().parse(request)
        jadic_serializer = Ja_DictionarySerializer(data=jadic_data)
        if jadic_serializer.is_valid():
            jadic_serializer.save()
            return JsonResponse({'message': 'The ja_text insert successfully!'}, status=status.HTTP_201_CREATED)
        return JsonResponse(jadic_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # function delete all list of ja-dictionary
    elif request.method == 'DELETE':
        count = Ja_Dictionary.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

# function search by ja to vi
@permission_classes([AllowAny])
@api_view(['GET', 'POST', 'DELETE'])
def jadictionary_search(request):
    if request.method == 'GET':
        title_name=request.GET['ja_text']

        jadictionarys = Ja_Dictionary.objects.raw("SELECT id, hiragana_text, vi_text FROM dsvn_dictionary_ja_dictionary WHERE (hiragana_text=%s OR kanji_text=%s OR katakana_text=%s)",[title_name, title_name, title_name])
        ja_serializer = Ja_DictionarySerializer(jadictionarys, many=True)
        
        return JsonResponse(ja_serializer.data, safe=False)

# function update ja-dic by id
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT'])
def jadictionary_update(request, pk):

    try: 
        jadic_data = Ja_Dictionary.objects.get(id=pk) 
    except Ja_Dictionary.DoesNotExist: 
        return JsonResponse({'message': 'The ja dictionary does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'PUT': 
        ja_data = JSONParser().parse(request) 
        jadic_serializer = Ja_DictionarySerializer(jadic_data, data=ja_data) 
        if jadic_serializer.is_valid(): 
            jadic_serializer.save() 
            return JsonResponse({'message': 'The record was updated successfully!'}, status=status.HTTP_202_ACCEPTED) 
        return JsonResponse(jadic_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# function delete ja-dic by id
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE'])
def jadictionary_delete(request, pk):

    try: 
        ja_dic = Ja_Dictionary.objects.get(pk=pk) 
    except Ja_Dictionary.DoesNotExist: 
        return JsonResponse({'message': 'The ja dictionary does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'DELETE': 
        ja_dic.delete() 
        return JsonResponse({'message': 'The row ja dictionary was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)  

# class translate string with google api
@permission_classes([AllowAny])
class GoogleTranslateView(APIView):
    def post(self, request):
        LANGUAGE_INPUT = JAPANESE
        LANGUAGE_OUTPUT = VIETNAMESE

        translator = Translator()
        message = request.GET["message"]
        language_input = translator.detect(message)

        if language_input.lang == VIETNAMESE:
            LANGUAGE_INPUT = VIETNAMESE
            LANGUAGE_OUTPUT = JAPANESE
        jatranslated = translator.translate(message, src=LANGUAGE_INPUT, dest=LANGUAGE_OUTPUT)
        
        return JsonResponse({'message': jatranslated.text}, status=status.HTTP_201_CREATED) 

# class translate file import
@permission_classes([AllowAny])
class TranslateFileView(APIView):
    def post(self, request):
        translator = Translator()
        
        try:
            f = open(FILE_IMPORT, READ_FILE, encoding=UTF8)
            if f.mode == READ_FILE:
                contents = f.read()
                result = translator.translate(contents, dest=VIETNAMESE)
                # print text to console
                print(result.text)
                with open(FILE_EXPORT, WRITE_FILE, encoding=UTF8) as f:
                    f.write(result.text)
            return JsonResponse({'message': "File import translate successfully!"}, status=status.HTTP_201_CREATED) 
        except:
            return JsonResponse({'message': "Can not find file import"}, status=status.HTTP_404_NOT_FOUND) 
        
# function common not using
# @api_view(['GET', 'POST', 'DELETE'])
# def tutorial_list(request):
#     if request.method == 'GET':
#         tutorials = DsvnDictionary.objects.all()
        
#         title = request.GET.get('title', None)
        
#         if title is not None:
#             tutorials = tutorials.filter(title__icontains=title)
        
#         tutorials_serializer = DsvnDictionarySerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
#         # 'safe=False' for objects serialization
 
#     elif request.method == 'POST':
#         tutorial_data = JSONParser().parse(request)
#         tutorial_serializer = DsvnDictionarySerializer(data=tutorial_data)
#         if tutorial_serializer.is_valid():
#             tutorial_serializer.save()
#             return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         count = DsvnDictionary.objects.all().delete()
#         return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
# @api_view(['GET', 'PUT', 'DELETE'])
# def tutorial_detail(request, pk):
#     try: 
#         tutorial = DsvnDictionary.objects.get(pk=pk) 
#     except DsvnDictionary.DoesNotExist: 
#         return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
#     if request.method == 'GET': 
#         tutorial_serializer = DsvnDictionarySerializer(tutorial) 
#         return JsonResponse(tutorial_serializer.data) 
 
#     elif request.method == 'PUT': 
#         tutorial_data = JSONParser().parse(request) 
#         tutorial_serializer = DsvnDictionarySerializer(tutorial, data=tutorial_data) 
#         if tutorial_serializer.is_valid(): 
#             tutorial_serializer.save() 
#             return JsonResponse(tutorial_serializer.data) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
#     elif request.method == 'DELETE': 
#         tutorial.delete() 
#         return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
# @api_view(['GET'])
# def tutorial_list_published(request):
#     tutorials = DsvnDictionary.objects.filter(published=True)
        
#     if request.method == 'GET': 
#         tutorials_serializer = DsvnDictionarySerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)  
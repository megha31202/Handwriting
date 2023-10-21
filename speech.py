import sys
import pygame
from pygame.locals import *
from pygame import Color
import os
import speech_recognition as sr

pygame.init()
clock = pygame.time.Clock()

# Create the Pygame window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Handwriting from Speech")
font = pygame.font.Font(None, 24)

# Variables
z = 0
mydraw = pygame.Surface((600, 300), pygame.SRCALPHA, 32)
pygame.draw.rect(mydraw, (255, 255, 255), (0, 0, 600, 300))
pygame.draw.line(mydraw, (163, 163, 163), (0, 100), (600, 100), 1)
pygame.draw.line(mydraw, (163, 163, 163), (0, 200), (600, 200), 1)

def display_text(text):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 320))

def draw_text(text):
    global mydraw
    mydraw = pygame.Surface((600, 300), pygame.SRCALPHA, 32)
    pygame.draw.rect(mydraw, (255, 255, 255), (0, 0, 600, 300))
    pygame.draw.line(mydraw, (163, 163, 163), (0, 100), (600, 100), 1)
    pygame.draw.line(mydraw, (163, 163, 163), (0, 200), (600, 200), 1)
    text_surface = font.render(text, True, (0, 0, 0))
    mydraw.blit(text_surface, (10, 10))

def save_speech_to_text(text):
    with open("content.txt", "a") as textfile:
        textfile.write(text + "\n")

def clear_content_file():
    with open("content.txt", "w"):
        pass

recognizer = sr.Recognizer()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))
    screen.blit(mydraw, (100, 50))

    # Listen for speech input
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Optional: Adjust for ambient noise
        audio = recognizer.listen(source)

    # Convert speech to text using Google Web Speech API
    try:
        user_input_text = recognizer.recognize_google(audio)
        print("You said:", user_input_text)

        # Save the speech text to content.txt
        save_speech_to_text(user_input_text)

        # Draw the recognized text on the drawing surface
        draw_text(user_input_text)

        # Display the recognized text on the screen
        display_text(user_input_text)

        # Check if the user said "stop" to stop listening
        if "stop" in user_input_text.lower():
            break

    except sr.UnknownValueError:
        print("Sorry, could not understand your speech.")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    pygame.display.update()

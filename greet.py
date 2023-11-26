import random

greetings = [
  "Sup, {name}! Have you solved any interesting math problems lately?",
  "Hey there, {name}! Did you know that math is the language of the universe?",
  "Hi, {name}! A mathematician is a device for turning coffee into theorems.",
  "Greetings, {name}! The only way to learn mathematics is to do mathematics.",
  "Howdy, {name}! Mathematics is not about numbers, equations, computations or algorithms; it is about understanding.",
  "Salutations, {name}! In mathematics, the art of proposing a question must be held of higher value than solving it.",
  "Yo, {name}! A good mathematician is a lazy one, for he will try to find the shortest path to his goal.",
  "What's up, {name}? Mathematics is the key and door to the sciences.",
  "Good day, {name}! Mathematics is the science of patterns, and we study patterns to understand the world around us.",
  "Nice to see you, {name}! Pure mathematics is, in its way, the poetry of logical ideas.",
  "Hello, {name}! Did you know that the square root of negative one is the most fascinating number in math?",
  "Hey there, {name}! Are you ready to integrate yourself into some math problems today?",
  "Hi, {name}! Why was the math book sad? Because it had too many problems.",
  "Greetings, {name}! Let's make like fractals and iterate!",
  "Howdy, {name}! The best way to understand math is to make it a part of your everyday life.",
  "Salutations, {name}! A circle is just a really, really, really polygon with an infinite number of sides.",
  "Yo, {name}! Math is like love; a simple idea, but it can get complicated.",
  "What's up, {name}? Math puns are the first sine of madness.",
  "Good day, {name}! I heard that parallel lines actually do meet, but they're just too busy to notice!",
  "Nice to see you, {name}! Math is like a language, the more you practice, the better you become at it.",
  "Hello, {name}! I have a joke about math, but it's so derivative, I'm afraid it won't function without a limit."
]


def greet_user(username):
  greeting = random.choice(greetings)
  user_greeting = greeting.format(name=username)
  return user_greeting

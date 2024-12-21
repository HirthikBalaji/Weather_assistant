import ollama
import requests
from ollama import ChatResponse,GenerateResponse

def get_weather(city):
    api_key = "5d95517ba78b331f79e6c28e1a7ab635"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q="  + city
    response = requests.get(complete_url)
    weather_data = response.json()

    return weather_data

messages=[{'role': 'system', 'content':
        'You are a Weather Expert now analyse this data and explain the weather! crisp clear and concise! not more than 100 words.'}]
while True:
    messages.append({'role': 'user', 'content':
        input(">>>")})
    response: ChatResponse = ollama.chat(
      'llama3.2',
      messages=messages,
      tools=[{
          'type': 'function',
          'function': {
            'name': 'get_current_weather',
            'description': 'Get the current weather for a city',
            'parameters': {
              'type': 'object',
              'properties': {
                'city': {
                  'type': 'string',
                  'description': 'The name of the city',
                },
              },
              'required': ['city'],
            },
          },
        },
      ],stream=True
    )
    print()
    available_functions = {
      'get_current_weather': get_weather}
    for chunk in response:
        if chunk.message.tool_calls is None:
            print(chunk['message']['content'], end='', flush=True)
        else:
            for tool in chunk.message.tool_calls:
                # Ensure the function is available, and then call it
                if function_to_call := available_functions.get(tool.function.name):
                    print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    if tool.function.arguments.values() is not None:
                        output = function_to_call(**tool.function.arguments)
                        print('Function output:', output)
                        # Add the function response to messages for the model to use
                        messages.append(chunk.message)
                        messages.append({'role': 'tool', 'content': "Here is the weather data in real-time :" + str(output),
                                         'name': tool.function.name})

                else:
                    print('Function', tool.function.name, 'not found')

        # Only needed to chat with the model using the tool call results

      # Get final response from model with function outputs
    final_response = ollama.chat('llama3.2', messages=messages,stream=True, tools=[{
          'type': 'function',
          'function': {
            'name': 'get_current_weather',
            'description': 'Get the current weather for a city',
            'parameters': {
              'type': 'object',
              'properties': {
                'city': {
                  'type': 'string',
                  'description': 'The name of the city',
                },
              },
              'required': ['city'],
            },
          },
        },
      ])
    print("RESULT:\n"+"-"*50+"\n")
    for chunk in final_response:
        print(chunk['message']['content'], end='', flush=True)
    print()
      # print('Final response:', final_response.message.content)

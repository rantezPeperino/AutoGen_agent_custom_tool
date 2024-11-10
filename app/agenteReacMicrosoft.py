import autogen
import requests
from typing import List, Dict, Any



def get_user_info(name: str) -> str:
    """Obtiene la información de un usuario basado en su nombre."""
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = response.json()
    
    # for user in users:
    #     if user['name'].lower() == name.lower():
    #         return str(user)
    
    return users


# Asegúrate de reemplazar 'your-openai-api-key' con tu clave real de OpenAI
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": ""
    }
]

# Definición del agente asistente
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0,
    },
    system_message="""Eres un asistente útil que responde preguntas sobre usuarios.
    Utiliza la función get_user_info para obtener información de usuarios cuando sea necesario.
    Responde siempre en español."""
)

# Definición del agente usuario
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    function_map={"get_user_info": get_user_info}
)

# Iniciamos la conversación
user_proxy.initiate_chat(
    assistant,
    message="Obtén el email y el código postal del usuario Leanne Graham"
)

# Para hacer otra consulta, descomentar la siguiente línea y ejecutar el script nuevamente
# user_proxy.send(assistant, "¿Cuál es el teléfono y mail de Chelsey Dietrich?")
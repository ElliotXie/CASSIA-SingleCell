import os
import json
import requests
from typing import Dict, Any, Optional

def call_llm(
    prompt: str,
    provider: str = "openai",
    model: str = None,
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    system_prompt: Optional[str] = None,
    additional_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Call an LLM from various providers and return the generated text.
    
    Args:
        prompt: The user prompt to send to the LLM
        provider: One of "openai", "anthropic", or "openrouter"
        model: Specific model from the provider to use (e.g., "gpt-4" for OpenAI)
        api_key: API key for the provider (if None, gets from environment)
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system prompt for providers that support it
        additional_params: Additional parameters to pass to the provider's API
    
    Returns:
        str: The generated text response
    """
    provider = provider.lower()
    additional_params = additional_params or {}
    
    # Default models for each provider if not specified
    default_models = {
        "openai": "gpt-3.5-turbo",
        "anthropic": "claude-3-sonnet-20240229",
        "openrouter": "openai/gpt-3.5-turbo",
    }
    
    # Use default model if not specified
    if not model:
        model = default_models.get(provider)
        if not model:
            raise ValueError(f"No model specified and no default available for provider: {provider}")
    
    # Get API key from environment if not provided
    if not api_key:
        env_var_names = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
        }
        env_var = env_var_names.get(provider)
        if env_var:
            api_key = os.environ.get(env_var)
            if not api_key:
                raise ValueError(f"API key not provided and {env_var} not found in environment")
    
    # Prepare messages format
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    # OpenAI API call
    if provider == "openai":
        try:
            import openai
        except ImportError:
            raise ImportError("Please install openai package: pip install openai")
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **additional_params
        )
        
        return response.choices[0].message.content
    
    # Anthropic API call
    elif provider == "anthropic":
        try:
            import anthropic
        except ImportError:
            raise ImportError("Please install anthropic package: pip install anthropic")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Format the prompt for Anthropic
        user_content = [{"type": "text", "text": prompt}]
        
        # Create the message with system as a string
        message_params = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user", 
                    "content": user_content
                }
            ]
        }
        
        # Add system prompt if provided
        if system_prompt:
            message_params["system"] = system_prompt
            
        # Add any additional parameters
        message_params.update(additional_params)
        
        # Call the API
        response = client.messages.create(**message_params)
        
        # Extract the text content from the response
        if hasattr(response, 'content') and len(response.content) > 0:
            content_block = response.content[0]
            if hasattr(content_block, 'text'):
                return content_block.text
            elif isinstance(content_block, dict) and 'text' in content_block:
                return content_block['text']
            else:
                return str(response.content)
        else:
            return "No content returned from Anthropic API"
    
    # OpenRouter API call
    elif provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **additional_params
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    else:
        raise ValueError(f"Unsupported provider: {provider}") 
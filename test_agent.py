#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test script to verify the agent works.
"""

import asyncio

from local_prompt_agent import Agent


async def main():
    """Test the agent."""
    print("🤖 Testing Local Prompt Agent...")
    print("=" * 50)
    
    # Initialize agent
    print("\n1. Initializing agent...")
    agent = Agent()
    print(f"   ✓ Agent initialized with model: {agent.config.backend.model}")
    
    # Health check
    print("\n2. Checking Ollama connection...")
    healthy = await agent.health_check()
    if healthy:
        print("   ✓ Connected to Ollama successfully!")
    else:
        print("   ✗ Cannot connect to Ollama. Is it running?")
        print("   Run: ollama serve")
        return
    
    # Test simple message
    print("\n3. Testing simple message...")
    response = await agent.execute("Say hello in 10 words or less")
    print(f"   Response: {response}")
    
    # Test streaming
    print("\n4. Testing streaming response...")
    print("   Response: ", end="", flush=True)
    async for token in agent.stream("Count from 1 to 5, just the numbers"):
        print(token, end="", flush=True)
    print()  # New line
    
    # Test Chinese
    print("\n5. Testing Chinese language...")
    response = await agent.execute("用繁體中文說你好")
    print(f"   Response: {response}")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Your agent is working perfectly!")
    print("\nTry it yourself:")
    print("  $ lpa chat")


if __name__ == "__main__":
    asyncio.run(main())

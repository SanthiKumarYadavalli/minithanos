from gemini import god_model


async def do(prompt):
    try:
        res = await god_model.generate(prompt)
        return res.text
    except Exception as e:
        print(f"Error occurred: {e}")
        return await do(prompt)

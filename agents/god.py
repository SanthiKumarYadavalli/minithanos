from gemini import god_model


async def do(prompt):
    try:
        res = await god_model.generate(prompt)
        return res.text
    except Exception as e:
        return str(e)

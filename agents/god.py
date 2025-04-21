from gemini import god_model


async def do(prompt):
    res = await god_model.generate(prompt)
    return res.text

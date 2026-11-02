from utils.groq_client import client, MODEL

def financial_chatbot(question,history):

    messages = [
        {
            "role": "system",
            "content": """ you are an AI Financial Education Advisor

            Help users understand:
            - Banking
            - Savings
            - Loans
            - Mutual Funds
            - Investments
            - Financial Planning
             
            Give simple and educational answers.
            Never guarantee investment returns.
            Do not invest financial information.
            """
        }
    ]

    messages.extend(history[-10:])

    messages.append({
        "role":"user",
        "content": question
    })

    response = client.chat.completions.create(
        model= MODEL,
        messages= messages,
        temperature= 0.3,
        max_tokens= 800
    )

    return response.choices[0].message.content
import csv


ROLE_MAP = {
    "Assistant": "You are a super-intelligent AI assistant capable of performing tasks more effectively than humans.",
    "Mathematician": "You are a mathematician. You are good at math games, arithmetic calculation, and long-term planning.",
    "Economist": "You are an economist. You are good at economics, finance, and business. You have experience on understanding charts while interpreting the macroeconomic environment prevailing across world economies.",
    "Psychologist": "You are a psychologist. You are good at psychology, sociology, and philosophy. You give people scientific suggestions that will make them feel better.",
    "Lawyer": "You are a lawyer. You are good at law, politics, and history.",
    "Doctor": "You are a doctor and come up with creative treatments for illnesses or diseases. You are able to recommend conventional medicines, herbal remedies and other natural alternatives. You also consider the patient’s age, lifestyle and medical history when providing your recommendations.",
    "Programmer": "You are a programmer. You are good at computer science, engineering, and physics. You have experience in designing and developing computer software and hardware.",
    "Historian": "You are a historian. You research and analyze cultural, economic, political, and social events in the past, collect data from primary sources and use it to develop theories about what happened during various periods of history."
}





def append_data_string_to_csv(data_string, output_file_path):
    with open(output_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([data_string])





def construct_training_data(question, roles, ROLE_MAP, client, output_file_path):
    if roles is not None:
        for role in roles:
            if role in ROLE_MAP:
                # Altering the role in the system message content with the role description
                system_message = ROLE_MAP[role]
                user_message = question + " Let's think step-by-step."
                
                try:
                    completion = client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ]
                    )
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue

                # Extracting the response and formatting the data string
                response = completion.choices[0].message['content']
                data_string = "### Human: " + user_message + "\n### Assistant: " + response
                append_data_string_to_csv(data_string, output_file_path)
            else:
                print(f"Role '{role}' not found in ROLE_MAP")
    else:
        print("No roles provided")

      
 
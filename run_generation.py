import data_generation


QUERY = "" 

ROLES = ["Assistant", "Assistant", "Assistant", "Assistant"]
#need function that gives us the role description based off of the key 

def main():
    construct_training_data(QUERY, ROLES)
    


if __name__ == "__main__":
    main()


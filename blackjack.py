import random
import sys
import os

#function to read money from the file
def read_money():
    if not os.path.exists("money.txt"):
        #create the file with a default value if it doesn't exist
        with open("money.txt", "w") as file:
            file.write("100.0")
    with open("money.txt", "r") as file:
        return float(file.read().strip())

#function to write money to the file
def write_money(amount):
    with open("money.txt", "w") as file:
        file.write(f"{amount:.2f}")

#function to draw a card
def drawcard():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                   "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
    deck = [{'rank': rank, 'suit': suit, 'value': card_values[rank]} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck.pop()

#function when player wins
def playerwin(playerscore, dealerscore, bet, money):
    print("\nCongratulations! You win.")
    print(f"Player score: {playerscore}")
    print(f"Dealer score: {dealerscore}")
    winnings = round(bet * 1.5, 2)  #blackjack payout ratio of 3:2
    money += winnings
    print(f"Money: {money:.2f}")
    write_money(money)
    return play_again(money)

#function when player loses
def playerlose(playerscore, dealerscore, bet, money):
    print("\nSorry. You lose.")
    print(f"Player score: {playerscore}")
    print(f"Dealer score: {dealerscore}")
    money -= bet
    print(f"Money: {money:.2f}")
    write_money(money)
    return play_again(money)

#function to ask if player wants to play again
def play_again(money):
    choice = input("\nPlay again? (y/n): ").lower()
    if choice == "y":
        return doblackjack(money)
    else:
        print("\nCome back soon!")
        print("Bye!")
        sys.exit()

#main Blackjack logic
def doblackjack(money):
    print("\n===========================")
    print("BLACKJACK!")
    print("Blackjack payout is 3:2\n")
    print(f"Money: {money:.2f}")

    #prompt user for bet
    while True:
        try:
            bet = int(input("Bet amount: "))
            if bet < 5 or bet > money:
                raise ValueError("Invalid bet amount.")
            break
            if bet > 1000:
                raise ValueError("Bet too high, big spender.")
            break
        except ValueError as e:
            print(e)
            continue

    playerscore = 0
    dealerscore = 0
    playercards = []
    dealercards = []

    #initial card draws
    playercards.append(drawcard())
    playercards.append(drawcard())
    dealercards.append(drawcard())
    dealercards.append(drawcard())

    playerscore = sum(card['value'] for card in playercards)
    dealerscore = sum(card['value'] for card in dealercards)

    print("\nDEALER'S SHOW CARD:")
    print(f"{dealercards[0]['rank']} of {dealercards[0]['suit']}")
    print("\nYOUR CARDS:")
    for card in playercards:
        print(f"{card['rank']} of {card['suit']}")

    #player turn
    while True:
        hitorstand = input("\nHit or stand? (hit/stand): ").lower()
        if hitorstand == "hit":
            new_card = drawcard()
            playercards.append(new_card)
            playerscore = sum(card['value'] for card in playercards)
            print(f"\nYou drew: {new_card['rank']} of {new_card['suit']}")
            print(f"Your total score is now: {playerscore}")

            if playerscore > 21:
                return playerlose(playerscore, dealerscore, bet, money)
        elif hitorstand == "stand":
            break
        else:
            print("Invalid entry. Please choose 'hit' or 'stand'.")

    #dealer turn
    print("\nDEALER'S CARDS:")
    for card in dealercards:
        print(f"{card['rank']} of {card['suit']}")
    while dealerscore < 17:
        new_card = drawcard()
        dealercards.append(new_card)
        dealerscore = sum(card['value'] for card in dealercards)
        print(f"Dealer drew: {new_card['rank']} of {new_card['suit']}")

    print(f"\nYOUR POINTS: {playerscore}")
    print(f"DEALER'S POINTS: {dealerscore}")

    #determine outcome
    if dealerscore > 21 or playerscore > dealerscore:
        return playerwin(playerscore, dealerscore, bet, money)
    elif dealerscore > playerscore:
        return playerlose(playerscore, dealerscore, bet, money)
    else:
        print("\nIt's a tie!")
        return play_again(money)

#main function
def main():
    money = read_money()  #read the player's money from the file
    doblackjack(money)

if __name__ == "__main__":
    main()

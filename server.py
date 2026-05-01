




def main():
    # create a listening socket
    # accept sockets on a new thread, up to some room limit.
    # within the accept thread, read UDP packets for player inputs
    # interpret those inputs and apply them.
    # send occasional TCP update packets to the clients, telling them the game state.
    pass

if __name__ == "__main__":
    main()
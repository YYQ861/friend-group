assert my_group.size() == 4, "Group should have 4 members"
    assert my_group.average_age() == 28.75, "Average age of the group is incorrect!"
    assert my_group.number_of_connections("Nash") == 1, "Nash should only have one relation"
    print("All assertions have passed!")
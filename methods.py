def set_who_asks(users, askser):
	for user in users:
		user.is_asking = False
	askser.is_asking = True
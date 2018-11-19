'''
This file is only being used to test the effectiveness of *args and **kwargs

'''

def unpredictable_func(a):
	if a % 2 == 0:
		return ['item1a', 'item1b']
	else:
		return ['item1a', 'item1b', 'item2a', 'item2b']





unpred_list1 = unpredictable_func(4)
unpred_list2 = unpredictable_func(5)

test_result1 = dependent_func(unpred_list1)
test_result2 = dependent_func(unpred_list2)

test_result1[0]
test_result2[0]
len(test_result1)
len(test_result2)

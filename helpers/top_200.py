import sys

def potato(path):
	dic = {}
	f = open(path,'r')
	for x in f:
		ok = x.rstrip().split(',')
		fname,tag = ok[0],ok[1]
		if tag in dic:
			dic[tag] += 1
		else:
			dic[tag] = 1
	return dic


if __name__ == "__main__":
	path = sys.argv[1]
	ret = potato(path)
	lex = sorted(ret,key = ret.get,reverse=True)
	for x in lex:
		print x,ret[x]

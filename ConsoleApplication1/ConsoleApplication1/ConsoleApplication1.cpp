#include <iostream>
#include <fstream>
#include <vector>
#include <deque>
#include <string>
#include <map>
#include <math.h>

using namespace std;
int main()
{
	vector<string> arr = vector<string>();
	arr.reserve(8416);
	fstream file = fstream("expanded.txt");
	string str;
	while (std::getline(file, str))
	{
		arr.push_back(str);
	} 
	cout << "end rendering" << endl;


	

	return 0;
}


class C {
public:
	int W = 0;
	float H = 0;
	deque<string[]> collection = {};
	
	void update() {
		map<string, int> v = {};
		for (int i = 0; i < collection.size; i++)
		{
			for (int j = 0; j < collection[i]->size; j++)
			{
				string str= collection[i][j];
				if (in(keys(v), str)) {
					v[str] += 1;
				}
				else {
					v[str] = 1;
				}
			}
		}

		W = keys(v).size;
		H = sum(value(v)) / W;
	}

	static float profit(float H, int W, float _r) {
		return H / powf(W, (_r - 1));
	}
	
	static map<float, int> get_H_W(deque<string[]> _collection) {
		map<string, int> v = {};
		for (int i = 0; i < _collection.size; i++)
		{
			for (int j = 0; j < _collection[i]->size; j++)
			{
				string str = _collection[i][j];
				if (in(keys(v), str)) {
					v[str] += 1;
				}
				else {
					v[str] = 1;
				}
			}
		}

		return map<float, int>{sum(value(v)) / keys(v).size = keys(v).size};
	}

	template<typename T>
	static bool in(deque<T> arr, T element) {
		for (int i = 0; i <=arr.size; ++i)
		{
			if (arr[i]==element) {
				return true;
			}
		}
		return false;
	}
	template<typename T1, typename T2>
	static deque<T1> keys(map<T1, T2> map) {
		deque<T1> keys = {};
		for (auto it = map.begin(); it != map.end(); ++it)
		{
			keys.push_back(it->first)
		}
		return keys
	}

	template<typename T1, typename T2>
	static deque<T2> value(map<T1, T2> map) {
		deque<T2> value = {};
		for (auto it = map.begin(); it != map.end(); ++it)
		{
			value.push_back(it->second)
		}
		return value
	}

	template<typename T>
	static float sum(deque<T> arr) {
		float n = 0;
		for (int i = 0; i < arr.size; ++i)
		{
			n+=arr[i]
		}
		return n;
	}
};



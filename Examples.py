helloworld="""#include<iostream>
using namespace std;

int main(){
    cout<<"Hello, World!";
    return 0;
}"""

search="""#include<iostream>
using namespace std;

int main(){
    int length, where, findtext;
    cin>>length;
    int array[length];
    for(int i=0;i<length;i++){
        cin>>array[i];
    }
    cin>>findtext;
    for(int i=0;i<length;i++){
        if(array[i] == findtext){
            where=i;
            break;
        }
    }
    cout<<where;
    return 0;
}"""

binarysearch="""#include<iostream>
#include<vector>
using namespace std;

int BinarySearch(const vector<int>& nums,int target){
    int low=0, mid=0, high=nums.size()-1;
    while (left <= right) {
        mid = low + ((high-low)/2);
        if (nums[mid] > target){
            high=mid-1;
        }else if(nums[mid] < target){
            low=mid+1;
        }else{
            return mid;
        }
    }
    return -1;
}

int main(){
    vector<int> nums;
    int size, target, input;
    cin>>size;
    for(int i=0;i<size;i++){
        cin>>input;
        nums.push_back(input);
    }
    cin>>target;
    cout<<BinarySearch(nums,target);
    return 0;
}
"""

rainbow="""#include<iostream>
#include<windows.h>
#include<conio.h>
#include<vector>
using namespace std;
#define ConsoleHandle GetStdHandle(STD_OUTPUT_HANDLE)

int main(){
    vector<int> colorHex;
    for(int i=0;i<0xff;i++){
        colorHex.push_back(i);
    }
    while (true){
        for(const auto& i:colorHex){
            Sleep(50);
            SetConsoleTextAttribute(ConsoleHandle,i);
            cout<<"This text will rainbow"<<endl;
        }
    }
    return 0;
}"""
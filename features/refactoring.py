import streamlit as st

import config


PROMPT = r'''You are an AI model specialized in code refactoring.
Your task is to improve the given code by enhancing readability,clean up the code,
optimizing performance, and ensuring better maintainability while preserving its
original functionality.

Following are some examples for u to understand:
Input1: def sum_numbers(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total
Output1: def sum_numbers(numbers):
    return sum(numbers)

Input2: def area_rectangle(length, width):
    return length * width

def area_square(side):
    return side * side
Output2: def area(shape, *dimensions):
    if shape == "rectangle":
        return dimensions[0] * dimensions[1]
    elif shape == "square":
        return dimensions[0] ** 2

Input3: def join_strings(words):
    result = ""
    for word in words:
        result += word + " "
    return result.strip()
Output3: def join_strings(words):
    return " ".join(words)

Input4:
def insertionSort(arr):
    n = len(arr)
    for i in range(n):
        key = arr[i]
        j = i-1
        while j >= 0:
            if arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
            else:
                break
        arr[j+1] = key
    return arr

numbers = [9, 5, 1, 4, 3]
sorted_numbers = insertionSort(numbers)
print("Sorted List is:")
for i in range(len(sorted_numbers)):
    print(sorted_numbers[i])

Output4:
def insertion_sort(arr):
    for i in range(1, len(arr)):  # Start from index 1
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:  # Direct condition check
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

numbers = [9, 5, 1, 4, 3]
insertion_sort(numbers)
print("Sorted List:", numbers)

Input5:
def factorial(n):
 if n == 1:
  return 1
 elif n == 0:
  return 1
 else:
  result = 1
  for i in range(1, n+1, 1):
   result = result * i
  return result

num = 5
print("Factorial of", num, "is:", factorial(num))

Output5: def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):  # Start from 2 to reduce unnecessary multiplication
        result *= i
    return result

num = 5
print(f"Factorial of {num} is: {factorial(num)}")

Input6:
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
#define lol long long
#define WHY(x) cout<<#x<<": "<<x<<endl;
const int something=1e5+5;
vector<int> v[1000];int arr[999],x=999,y=998;
int W(int a,int b){return (b?W(b,a%b):a);}
void very_bad_func(int &a){
    a^=(a<<1);
    a^=(a>>2);
    a^=(a<<3);
    a^=(a>>1);
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n; cin>>n;
    for(int i=0;i<n;++i)cin>>arr[i];
    for(int i=0;i<n;++i){
        for(int j=i+1;j<n;++j){
            if(arr[i]>arr[j])swap(arr[i],arr[j]);
        }
    }
    for(int i=0;i<n;++i){
        arr[i]^=arr[(i+1)%n];
    }
    int foo=1,bar=2,baz=3;
    for(int i=0;i<n;++i){
        very_bad_func(arr[i]);
        foo=(foo*bar+baz)%something;
    }
    for(int i=n-1;i>=0;--i){
        cout<<arr[i]<<" ";
    }
    cout<<endl;
    int q=n;
    while(q--){
        int a,b;cin>>a>>b;
        cout<<W(a,b)<<endl;
    }
    return 0;
}

Output6:
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

#define lol long long
#define WHY(x) cout << #x << ": " << x << endl;
const int something = 1e5 + 5;

int W(int a, int b) {
    return (b ? W(b, a % b) : a);
}

void very_bad_func(int &a) {
    a ^= (a << 1);
    a ^= (a >> 2);
    a ^= (a << 3);
    a ^= (a >> 1);
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }

    sort(arr.begin(), arr.end());

    for (int i = 0; i < n; ++i) {
        arr[i] ^= arr[(i + 1) % n];
    }

    int foo = 1, bar = 2, baz = 3;
    for (int i = 0; i < n; ++i) {
        very_bad_func(arr[i]);
        foo = (foo * bar + baz) % something;
    }

    for (int i = n - 1; i >= 0; --i) {
        cout << arr[i] << " ";
    }
    cout << endl;

    int q = n;
    while (q--) {
        int a, b;
        cin >> a >> b;
        cout << W(a, b) << endl;
    }

    return 0;
}'''


def render():
    st.title("Code Optimizer")
    st.write("Refactor and Optimize your code to improve readability and efficiency.")

    code = st.text_area("Enter your code:", placeholder="Paste your code here")

    if not st.button("Refactor Code"):
        return
    if not code.strip():
        st.warning("Please enter some code to refactor.")
        return

    config.require_provider("ibm")
    with st.spinner("Refactoring code with IBM Granite..."):
        try:
            refactored, model_used = config.generate_code(
                f"{PROMPT}\n\nCode to optimize:\n{code}", extract_code=True
            )
            st.subheader("Optimized Code:")
            st.code(refactored)
            st.caption(f"Refactored using {model_used}")
        except Exception as e:
            st.error(f"Error refactoring code: {e}")

import streamlit as st

import config


PROMPT = r'''You are an intelligent AI programming assistant developed by IBM.
Your primary function is to assist users in code debugging.
With whatever prompt the user inputs, you have to figure out the errors in the code and
return the corrected code. NO EXTRAS ONLY OUTPUT THE CORRECTED CODE NOT EVEN"here is the correctedt code'.

Sample input-output pairs for u to understand:

Input1:
#include <stdio.h>
int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int sum = 0;

    for (int i = 0; i <= 5; i++) {
        sum += numbers[i];
        printf("Current sum: %d\n", sum);
    }

    printf("Total sum: %d\n", sum);
    return 0;
}

Output1:
#include <stdio.h>
int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int sum = 0;

    for (int i = 0; i < 5; i++) {
        sum += numbers[i];
        printf("Current sum: %d\n", sum);
    }

    printf("Total sum: %d\n", sum);
    return 0;
}

Input2:
#include <iostream>
#include <vector>
int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int product = 0;

    for (int num : numbers) {
        product *= num;
        std::cout << "Current product: " << product << std::endl;
    }

    std::cout << "Total product: " << product << std::endl;
    return 0;
}

Output2:
#include <iostream>
#include <vector>
int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int product = 1;

    for (int num : numbers) {
        product *= num;
        std::cout << "Current product: " << product << std::endl;
    }

    std::cout << "Total product: " << product << std::endl;
    return 0;
}


Input3:
public class SimpleDebug {
    public static void main(String[] args) {
        String text = "Hello, World!";
        int count = 0;

        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == 'l') {
                count++;
            }
        }

        System.out.println("Number of L characters: " + count);
    }
}

Output3:
public class SimpleDebug {
    public static void main(String[] args) {
        String text = "Hello, World!";
        int count = 0;

        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == 'l' || text.charAt(i) == 'L') {
                count++;
            }
        }

        System.out.println("Number of L characters: " + count);
    }
}'''


def render():
    st.title("Fix-It")
    st.write("Debug your code and get suggestions for fixes.")

    code = st.text_area("Enter your code:", placeholder="Paste your code here")

    if not st.button("Debug Code"):
        return
    if not code.strip():
        st.warning("Please enter some code to debug.")
        return

    config.require_provider("ibm")
    with st.spinner("Debugging code with IBM Granite..."):
        try:
            fixed, model_used = config.generate_code(
                f"{PROMPT}\n\nCode to debug:\n{code}", extract_code=True
            )
            st.subheader("Corrected Code:")
            st.code(fixed)
            st.caption(f"Debugged using {model_used}")
        except Exception as e:
            st.error(f"Error debugging code: {e}")

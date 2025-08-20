"""Base implementation for the prefix function.

See https://cp-algorithms.com/string/prefix-function.html for more details.
"""


def find_positions_of_query(text: str, query: str) -> list[int] | None:
    """Find the positions of the query string in the text.

    This uses the prefix function and Knuth-Morris-Pratt algorithm.

    It works as follows:
    1. Concatenate query and text with some intermediate character not in text
    2. Construct the prefix function F over the concatenation
    3. Iterate through each index i > |query|+1, and check whether F[i]==|query|. If it is, it's a match.

    The prefix function F of a string s is an array of length |s|. F[i] is defined as the length of the longest proper prefix in s[0..i] is also a suffix.
    For instance:
        Let s = "abcfabcg"
        Then F = [0, 0, 0, 0, 1, 2, 3, 0]
    or
        Let s = "abcabzabcabfz"
        Then F = [0, 0, 0, 1, 2, 0, 1, 2, 3, 4, 5, 0, 0]
    or
        Let s = "abadababz"
        Then F = [0, 0, 1, 0, 1, 2, 3, 2, 0]

    abad abab
    jX     jX
    1. set j = F[i-1] = 3. s[3] = d != b = s[i], move forward
    2. j <- F[j-1] = F[2] = 1 (aba)
        2.1 s[j] = s[1] = b == b = s[i]
        Thus set F[i] = F[2] + 1 = 2

    It can be constructed in linear time O(|s|) iteratively for i>=1 as follows, starting with F[0]=0:
    1. if s[i] == s[F[i-1]], then F[i] = F[i-1] + 1.
        Example: s as above. If i = 6, then F[i-1]=2, and s[F[i-1]] is the letter after the prefix, which we compare against the new, rightmost letter.
    2. We need to find see if there is a shorter prefix matching this new suffix -- specifically one shorter than the previous index's max prefix length F[i-1].
        - We need to efficiently search for a prefix length `j` where two conditions hold:
            s[j] == s[i]   <- the letter after the prefix matches the new, rightmost letter
            else move back j = F[j-1], i.e. the length of the match of the next shorter prefix.

    :param text: Text to search in.
    :param query: String to query within the text.
    :return: The indices on which query matched in text, or None if no matches.
    """
    if len(query) > len(text):
        return None

    concatenation = f"{query}#{text}"
    prefix_func = _create_prefix_func(concatenation)

    matches = []
    relevant_prefix_func = prefix_func[len(query) + 1 :]
    for index, match_length in enumerate(relevant_prefix_func):
        # Since the concatenation string # is unique, a len(query) match length can
        # only be achieved by exact matching the query
        if match_length == len(query):
            # Prefix function marks the end index of the match
            matches.append(index - (len(query) - 1))

    return matches or None


def _create_prefix_func(string: str) -> list[int]:
    """Create a prefix function for a string.

    :param string: String to create prefix function for.
    :return: The function values.
    """
    prefix_func: list[int] = [-1] * len(string)

    # By definition, length of longest proper prefix matching a suffix is 0 if there's one element only (index 0)
    prefix_func[0] = 0

    for i, char in enumerate(string):
        if i == 0:
            continue

        cur_max_length = prefix_func[i - 1]
        # Check shorter suffixes, until we find one that yields a match with the last item
        while cur_max_length > 0 and string[cur_max_length] != char:
            # We "zoom in" on the current prefix and try to split it again by doing this
            cur_max_length = prefix_func[cur_max_length - 1]

        if string[cur_max_length] == char:
            # We found a possible extension by going backwards
            cur_max_length += 1

        prefix_func[i] = cur_max_length

    assert all(val != -1 for val in prefix_func)

    return prefix_func

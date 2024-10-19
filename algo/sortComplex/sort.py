def binary_search(arr , a):
    low,high = 0, len(arr)
    while low < high:
        mid = int((low + high)/2)
        

        if arr[mid] == a :
            return True
        elif arr[mid] > a :
            if mid == high:
                return False
            high = mid
        elif arr[mid] < a:
            if mid == low:
                return False
            low = mid
    return False

def bubble_sort(arr):
    arr_len = len(arr)
    
    for i in range(arr_len):
        ordered = True
        for j in range(arr_len-i-1):
            if arr[j] > arr[j+1]:
                arr[j+1], arr[j] = arr[j], arr[j+1]
                ordered = False
        if ordered:
            break
    return arr

def insert_sort(arr):
    arr_len = len(arr)
    if arr_len <= 1:
        return arr
    arr[0], arr[1] = arr[1], arr[0]
    for i in range(2,arr_len):
        # insert arr[i] to arr[0:i]
        for j in range(i):
            # find the locatio
            if arr[i]<arr[j]:
                # get arr[i] and save it into tmp value
                tmp = arr[i]
                # move each element from [j,i] forward 
                while i > j :
                    arr[i] = arr[i-1]
                    i-=1
                # replace arr[j] with the tmp
                arr[j] = tmp
                break
            # if greater than all elements, then move i forward
    return arr

def merge(arr_a, arr_b):
    if arr_a == None:
        return arr_b
    if arr_b == None:
        return arr_a
    len_a = len(arr_a)
    len_b = len(arr_b)
    res = [0 for _ in range(len_a+len_b)]
    i,j,k = 0,0,0
    while i <= len_a and j<=len_b:
        if k == (len_a+len_b):
            break
        if i == len_a:
            res[k] = arr_b[j]
            j+=1
        elif j== len_b:
            res[k] = arr_a[i]
            i+=1
        else:
            if arr_a[i] > arr_b[j]:
                res[k] = arr_b[j]
                j+=1
            else:
                res[k] = arr_a[i]
                i+=1
        k+=1
    return res


def merge_sort(arr):
    arr_len = len(arr)
    if arr_len == 1:
        return arr
    mid = int(arr_len/2)
    left_arr = merge_sort(arr[0:mid])
    right_arr = merge_sort(arr[mid:arr_len])
    return merge(left_arr,right_arr)


def partition(arr, low, high):
    pivot = arr[high]
    i = low-1
    for j in range(low, high-1):
        if arr[j] <= pivot:
            i+=1
            arr[i], arr[j] = arr[j], arr[i]
        
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def quick_sort_helper(arr, low, high):
    if low < high:
        
        cut_off = partition(arr, 0,high)
        quick_sort_helper(arr, 0, cut_off-1)
        quick_sort_helper(arr, cut_off+1,high)

def quick_sort(arr, low = 0, high=0):
    quick_sort_helper(arr, 0, len(arr)-1)
    return arr


if __name__ == '__main__':
    sorted_arr = quick_sort([6,3,2,7,5])
    print(sorted_arr)
    res = binary_search(sorted_arr, 3)
    print(res)

            

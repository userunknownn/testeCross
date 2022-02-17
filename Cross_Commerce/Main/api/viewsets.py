import json, asyncio, aiohttp

from rest_framework import viewsets, status
from . import serializers
from rest_framework.response import Response
from Main.models import Numbers


class NumbersViewSet(viewsets.ModelViewSet):
   
    serializer_class = serializers.Numbers_Serializer

    def get_queryset(self):
        numbers_within_pages = all_numbers_within_pages()
        ordered_numbers = mergesort(numbers_within_pages)
        
        numbers_list = []
        for current_number in ordered_numbers:
        
            numbers_list.append(Numbers(number=current_number))
              
        return numbers_list

#  merge sort
def merge(left,right):	#merges 2 sorted lists together 

	result = [] 
	i, j = 0, 0 
	
	#Goes through both lists 
	while i < len(left) and j < len(right):	
	#Adds smaller element of the lists to the final list 
		if left[i] <= right[j]:
			result.append(left[i]) 
			i += 1
		else:
			result.append(right[j]) 
			j += 1

	result += left[i:] 
	result += right[j:] 
	
	return result

def mergesort(lst):

	#if there's only 1 element, no need to sort 
	if len(lst) < 2:
		return lst
	
	#breaks down list into 2 halves 
	middle = len(lst) // 2	

	#recursively splits and sorts each half	
	left = mergesort(lst[:middle])	
	right = mergesort(lst[middle:]) 

	#merges both sorted lists together 
	return merge(left, right)

#end mergesort    

           
def get_page(session, initial_page, last_page):
    number_pages = []

    pages = range(initial_page, last_page)
    
    for page in pages:
    
        #use_cross_commerce_api
        url      = use_cross_commerce_api(page)
        number_pages.append(asyncio.create_task(session.get(url)))
    
    return number_pages

async def get_pages(initial_page, last_page):
    async with aiohttp.ClientSession(trust_env=True) as session:
    
        number_pages = get_page(session, initial_page, last_page)
        responses = await asyncio.gather(*number_pages)
        
        pages_results = []
        
        for response in responses:
             pages_results.append(await response.json())
             
        return pages_results

#get the page number with the request
def get_page_with_error(session, pages):
    number_pages = []
    
    for page in pages:
        url      = use_cross_commerce_api(page)
        number_pages.append(asyncio.create_task(session.get(url)))
    
    return number_pages


async def get_pages_with_error_again(pages):
    async with aiohttp.ClientSession(trust_env=True) as session:
    
        number_pages = get_page_with_error(session, pages)
        responses = await asyncio.gather(*number_pages)
        
        pages_results = []
        for response in responses:
            pages_results.append(await response.json())

             
        return pages_results

def all_numbers_within_pages():

    initial_page      = 1
    last_page         = 3501

    empty_page        = {'numbers': []}
    pages             = []
    pages_with_error  = []
    
    while(True):
    
        pages_request   = asyncio.run(get_pages(initial_page, last_page))
                
        pages.append(pages_request)        
                
        if pages_request[-1] == empty_page:
            break

        initial_page = last_page + 1 
        last_page    = last_page + 3500
    
     
    # to join the pages requested in one list
    new_page_set = []
    
    for page_set in pages:
        for page in page_set:
            new_page_set.append(page)
        
    pages = new_page_set
            

    page_counter     = 0
    
    for page in pages:
        
        if 'error' in page:
            pages_with_error.append(page_counter)
            
        page_counter += 1

        
    while(pages_with_error != []):
        pages_with_error_request = []
            
        error_pages_request   = asyncio.run(
                                    get_pages_with_error_again(
                                        pages_with_error
                                    )
                                )
            
           
        sucess_page_counter = 0
        
        # Catch the right value of the page in pages_with_error
        for page in error_pages_request:
            
            if 'numbers' in page:

                index_pages_with_error = pages_with_error[sucess_page_counter]
                page_info              = [page, index_pages_with_error]
            
                pages_with_error_request.append(page_info)   
               
            
            sucess_page_counter += 1   
        
        new_error_page_set = [] 
       
        counter = 0
        #end
        errors_to_remove = []
        for page in pages_with_error_request:
            errors_to_remove.append(page[1])
            
        page_counter     = 0
        pages_to_remove  = []
        
        #look for the index 
        # if the number in the pages_with_error is 
        # in the list of the of the sucess requests 
        # remove it 
        for page in pages_with_error:
        
            if page in errors_to_remove:
                    pages_to_remove.append(page_counter)
                    
            page_counter += 1
            
        
        assert_value = 0     
        
        for page in pages_to_remove:
        
            page = page - assert_value
            
            pages_with_error.pop(page)
       
            assert_value += 1    

        for page in pages_with_error_request:
            page_index   = page[1]
            page_content = page[0]
            
            pages[page_index] = page_content
        

    #   This is how to cut down the empty pages     

    first_empty_page = []
    page_counter     = 0
    

    for page in pages:

        if 'numbers' in page:
            
            if page['numbers'] == []:
                if len(first_empty_page) == 0:
                    first_empty_page.append(page_counter)
        
        page_counter += 1
    
    if len(first_empty_page) > 0 : 
               
        cut = first_empty_page[0]
        
        #cutting the numbers list at the first empty page 
        pages = pages[0:cut]   

    all_numbers = []
    
    for page in pages:
        for number in page['numbers']:
            all_numbers.append(number)
        
    return all_numbers


def use_cross_commerce_api(page):
    
    base_url   = "http://challenge.dienekes.com.br/api/numbers?page="
   
    url        = base_url + str(page)
    
    return url



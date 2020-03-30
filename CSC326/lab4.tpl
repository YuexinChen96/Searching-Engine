<html>
<head><title>Searching</title>
</head>
<body>



<form action="/keywords" method="get">
<img src="http://searchtagz.com/wp-content/uploads/2013/10/search-engine-optimization.jpg" width=350>
<p>
Search: <input name="keywords" type="text" />
<input value="Search" type="submit" />
</p>

%if not flag:
	<td style="width:20%;">Search for:&nbsp;<span style="background-color:yellow;">{{word}}</span></td>
%else:
	<td style="width:20%">Do you mean:&nbsp;<span style="background-color:yellow;">{{word_l}}</span></td>
%end
</form>





%for x in range(len(pages[c_page - 1])):
		<p>
			<a href={{pages[c_page-1][x]}}>{{pages[c_page-1][x]}}</a>
		</p>
%end

%if len(pages)<=5:
%o_page = range(len(pages)+1)[1:]
%elif c_page <= 3:
%o_page = range(6)[1:]
%elif c_page<=len(pages)-2:
%o_page = range(c_page+3)[c_page-2:c_page+3]
%else:
%o_page = range(len(pages)+1)[len(pages)-4:]
%end


<form action="search" method="get">
%if c_page == 1:
%for x in o_page:
	<input name="page_no" value={{x}} type="submit" />
%end
	<input name=">>" value=">>" type="submit" />
%elif c_page == len(pages):
	<input name="<<" value="<<" type="submit" />
%for x in o_page:
	<input name="page_no" value={{x}} type="submit" />
%end
%else:
	<input name="<<" value="<<" type="submit" />
%for x in o_page:
	<input name="page_no" value={{x}} type="submit" />
%end
	<input name=">>" value=">>" type="submit" />
%end

</form>

<form>
<input value = 'To page:' type ="submit" />
<input name = 'page_num' type = 'text' style = "width:30px;"/>
</form>




</body>
</html>


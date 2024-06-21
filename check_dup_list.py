########## Check duplicate table/view #############
dup_table= {x for x in list_table_result if list_table_result.count(x) > 1} # Check duplicate table
dup_view= {x for x in list_view_result if list_view_result.count(x) > 1} # Check duplicate view

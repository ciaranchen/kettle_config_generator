t1 = r"""
<field>
  <name>{name}</name>
  <type>None</type>
  <format/>
  <currency/>
  <decimal/>
  <group/>
  <nullif/>
  <ifnull/>
  <position>-1</position>
  <length>-1</length>
  <precision>-1</precision>
  <trim_type>none</trim_type>
  <repeat>N</repeat>
</field>
"""

t2 = r"""
<field>
<name>{name}</name>
<type>String</type>
<format/>
<currency/>
<decimal/>
<group/>
<nullif/>
<trim_type>both</trim_type>
<length>-1</length>
<precision>-1</precision>
</field>
"""

t3 = r"""
<field>
<name>{name}</name>
<type>String</type>
<format/>
<currency/>
<decimal/>
<group/>
<nullif/>
<trim_type>both</trim_type>
<length>-1</length>
<precision>-1</precision>
</field>
"""

t4 = r"""
<field>
<in_stream_name>{name}</in_stream_name>
<out_stream_name/>
<trim_type>none</trim_type>
<lower_upper>none</lower_upper>
<padding_type>none</padding_type>
<pad_char/>
<pad_len/>
<init_cap>no</init_cap>
<mask_xml>none</mask_xml>
<digits>none</digits>
<remove_special_characters>crlf</remove_special_characters>
</field>
"""

t5 = r"""
<field>
<in_stream_name>{name}</in_stream_name>
<out_stream_name/>
<use_regex>no</use_regex>
<replace_string>&#x24;&#x7b;SPLIT_&#x7d;</replace_string>
<replace_by_string/>
<set_empty_string>Y</set_empty_string>
<replace_field_by_string/>
<whole_word>no</whole_word>
<case_sensitive>no</case_sensitive>
</field>
"""

templateFields = [
  (t1, "get_datafile_input"), 
  (t2, "out_put_end_file"),
  (t3, "out_put_file_bf"),
  (t4, "fields_change_first"),
  (t5, "fields_split")]


t6 = r"""
<field>
<in_stream_name>{name}</in_stream_name>
<out_stream_name/>
<use_regex>no</use_regex>
<replace_string/>
<replace_by_string/>
<set_empty_string>N</set_empty_string>
<replace_field_by_string/>
<whole_word>no</whole_word>
<case_sensitive>no</case_sensitive>
</field>
"""

t6_last = r"""
<field>
<in_stream_name>{name}</in_stream_name>
<out_stream_name/>
<use_regex>no</use_regex>
<replace_string>&#x7c;-&#x7c;</replace_string>
<replace_by_string/>
<set_empty_string>Y</set_empty_string>
<replace_field_by_string/>
<whole_word>no</whole_word>
<case_sensitive>no</case_sensitive>
</field>
"""

special_field = (
  "fields_split_second",
  t6, t6_last)

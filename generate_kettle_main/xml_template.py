
entry_template = """<entry>
      <name>{name}</name>
      <description/>
      <type>JOB</type>
      <specification_method>filename</specification_method>
      <job_object_id/>
      <filename>{path}{split}{name}{split}{name}_0.kjb</filename>
      <jobname/>
      <arg_from_previous>N</arg_from_previous>
      <params_from_previous>N</params_from_previous>
      <exec_per_row>N</exec_per_row>
      <set_logfile>N</set_logfile>
      <logfile/>
      <logext/>
      <add_date>N</add_date>
      <add_time>N</add_time>
      <loglevel>Nothing</loglevel>
      <slave_server_name/>
      <wait_until_finished>Y</wait_until_finished>
      <follow_abort_remote>N</follow_abort_remote>
      <expand_remote_job>N</expand_remote_job>
      <create_parent_folder>N</create_parent_folder>
      <pass_export>N</pass_export>
      <parameters>        <pass_all_parameters>Y</pass_all_parameters>
      </parameters>      <set_append_logfile>N</set_append_logfile>
      <parallel>N</parallel>
      <draw>Y</draw>
      <nr>0</nr>
      <xloc>{xloc}</xloc>
      <yloc>{yloc}</yloc>
    </entry>"""

start_hop = """
    <hop>
      <from>START</from>
      <to>{name}</to>
      <from_nr>0</from_nr>
      <to_nr>0</to_nr>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>Y</unconditional>
    </hop>
"""

end_hop = """
    <hop>
      <from>{name}</from>
      <to>END</to>
      <from_nr>0</from_nr>
      <to_nr>0</to_nr>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>N</unconditional>
    </hop>
"""

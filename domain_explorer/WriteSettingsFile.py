import staticValues
from collections import OrderedDict


class WriteSettingsFile:
    """
    WriteSettingsFile contains all methods for printing settings file in output.
    It will group sections found in wikipedia resources and each section will have a key that represents
    table's header.
    This file is organized like python dictionary, in this way user can easily fill all fields.
    In order to help user in this task, I will print an example wikipedia page where a section is found and
    I will also add all table's headers that are in "pyTableExtractor" dictionary.

    It's important to note strings printed in settings file:
    - sectionProperty: represent ontology property to map section.
    - one row for each table's header -->  "Header":"ontology property"
    """
    def __init__(self, all_sections, all_headers, all_list_sections, explorer_tools):
        """
        Instantiate class, read all parameters then start to print settings file

        :param all_sections: sections found in wikipedia resources
        :param all_headers: set that contains table's headers
        :param explorer_tools: explorer_tools class that will be useful for public methods.
        """
        # order dictionary by key
        self.all_sections = OrderedDict(sorted(iter(list(all_sections.items())), key=lambda x: x[0]))
        self.all_headers = all_headers
        self.all_list_sections = all_list_sections
        self.explorer_tools = explorer_tools
        self.language = explorer_tools.language
        self.resource = explorer_tools.resource
        self.toExtractTables = explorer_tools.toExtractTables
        self.toExtractLists = explorer_tools.toExtractLists
        # start to write
        try:
            self.write_sections_and_headers()
        except Exception as e:
            print(e)



    def write_sections_and_headers(self):
        """
        Method that create and start to print settings file. Each section has his own dictionary that contains
        all table headers.
        :return:
        """
        # Create new file
        domain_explored_file = open(staticValues.FILE_PATH_DOMAIN_EXPLORED, 'w')
        # Print file heading
        self.write_file_heading(domain_explored_file)

        self.write_table_sections_and_headers(domain_explored_file)

        self.write_list_section_names(domain_explored_file)

        domain_explored_file.write(staticValues.END_OF_FILE)
        domain_explored_file.close()
        
    def write_file_heading(self, domain_explored_file):
        """
        Write file heading.
        File heading holds information about user's parameters:
        - coding type.
        - domain explored.
        - chapter, language defined.
        - resource file, that contains all resources involved in user's research.
        - comments to facilitate user's work.
        :param domain_explored_file: reference to the output file
        :return:
        """
        domain_explored_file.write(staticValues.CODING_DOMAIN + "\n")
        domain_explored_file.write(staticValues.FIRST_COMMENT + "\n")
        domain_explored_file.write(staticValues.DOMAIN_TITLE + ' = "' + self.resource + '" \n')
        domain_explored_file.write(staticValues.CHAPTER + ' = "' + self.language + '" \n')
        domain_explored_file.write(staticValues.COLLECT_MODE + ' = "' + self.explorer_tools.collect_mode + '" \n')
        domain_explored_file.write(staticValues.TABLES_INCLUDED + ' = "' + self.toExtractTables + '" \n')
        domain_explored_file.write(staticValues.LISTS_INCLUDED + ' = "' + self.toExtractLists + '" \n')
        domain_explored_file.write(staticValues.RESOURCE_FILE + ' = "' + self.explorer_tools.get_res_list_file() + '" \n\n')
        #domain_explored_file.write(staticValues.COMMENT_SECTION_PROPERTY + "\n\n")
        domain_explored_file.write(staticValues.COMMENT_STRUCTURE + "\n\n")
        domain_explored_file.write(staticValues.COMMENT_FILLED_ELEMENT + "\n\n")

    def write_table_sections_and_headers(self, domain_explored_file):
        """
        Write sections and headers of tables data on file.
        :param domain_explored_file: reference to file writing to.
        :return:
        """

        for mapper, sections in list(self.all_sections.items()):
            domain_explored_file.write(mapper + "___TABLES" + " = {\n")
            for key, section_dict in list(sections.items()):
                # adjust key to print in output
                key = self.explorer_tools.replace_accents(key.replace(" ", "_").replace("-", "_"))
                # print comments and first line of section
                # domain_explored_file.write(staticValues.COMMENT_FOR_EXAMPLE_PAGE + section_dict["exampleWiki"] + "\n")
                # delete example page that is useless now
                del section_dict["exampleWiki"]
                # print section dictionary that contains all table headers.
                self.print_dictionary_on_file(mapper, domain_explored_file, key, section_dict)
            domain_explored_file.write("} \n")

    def print_dictionary_on_file(self, mapper, file_settings, section_name, section_dict):
        """
        Write dictionary in a file.
        :param mapper: reference to mapper used
        :param file_settings: reference to output file
        :param section_dict: section dictionary to print in file
        :param section_name: reference to section name of the table
        :return:
        """
        for key, value in list(section_dict.items()):
            if key == staticValues.SECTION_NAME_PROPERTY:
                file_settings.write("'" + staticValues.SECTION_NAME+section_name + "' : '" + value + "'" + ", \n")
            # don't print header already printed
            elif self.all_headers[mapper][key] != "printed":
                file_settings.write("'" + key + "': '" + value + "'" + ", \n")
                self.all_headers[mapper].__setitem__(key, "printed")

    def write_list_section_names(self, domain_explored_file):
        """
        Write section names of lists into the file.
        :param domain_explored_file: reference to file writing to.
        :return:
        """

        for mapper, sections in list(self.all_list_sections.items()):
            printed_keys=[]
            domain_explored_file.write("\n#Following are section mappings of lists found:\n")
            domain_explored_file.write("#Mapper used for the following are: "+mapper.split('___')[1]+"\n\n")
            domain_explored_file.write(mapper + "___LISTS" + " = {\n")
            for key, value in list(sections.items()):
                if key not in printed_keys:
                    # adjust key to print in output
                    key = self.explorer_tools.replace_accents(key.replace("'",""))
                    domain_explored_file.write("'" + key + "': '" + value + "'" + ", \n")
                    printed_keys.append(key)
            domain_explored_file.write("} \n")

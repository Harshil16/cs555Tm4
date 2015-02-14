/*
 * main.c
 *
 *  Created on: Feb 8, 2015
 *      Author: justin
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_valid(char* tag);

int main(int argc, const char* argv[] )
{
	FILE *gedcom_file;
	char line[1000];
	char parse_line[1000];
	char *token;

	char *level;
	char tag[4];

	gedcom_file = fopen (argv[1], "r");

	if(!gedcom_file){
		printf("File %s does not exist.", argv[1]);
		return(1);
	}

	while (fgets(line, sizeof(line), gedcom_file)) {
		strcpy(parse_line,line);
		token = strtok(parse_line," ");
		level = token;
		token = strtok(NULL," ");
		strcpy(tag,token);
		if(is_valid(tag)== 1){
			strcpy(tag,"Invalid Tag");
		}
		printf("%s\n%s\n%s\n\n", line, level, tag);

	}

	fclose(gedcom_file);

	return(0);
}

int is_valid(char* tag){
	int i =0;
	char *valid_tags[16]={"INDI",
			"NAME",
			"SEX",
			"BIRT",
			"DEAT",
			"FAMC",
			"FAMS",
			"FAM",
			"MARR",
			"HUSB",
			"WIFE",
			"CHIL",
			"DIV",
			"DATE",
			"TRLR",
			"NOTE"};
	for (i=0; i<16;i++){
		//printf("COMP: %s %s\n",tag,valid_tags[i]);
		if (strcmp(tag,valid_tags[i])== 0){
			return 0;
		}
	}
	return 1;
}

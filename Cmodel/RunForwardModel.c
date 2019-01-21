/*this will read model parameters from a file, and cooling history from a file, and save the model output to a new file*/

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<math.h>

/*this function uses thomas' aglorithm to solve a tridiagonal system*/
double thomas_alg(int n, double* a, double* b, double* c, double* d, double* x){
	
	int i;
	c[0]=c[0]/b[0];

	for (i=1; i<n-1; i++)
		c[i]=c[i]/(b[i]-a[i]*c[i-1]);

	d[0]=d[0]/b[0];
	
	for (i=1; i<n; i++)
		d[i]=(d[i]-a[i]*d[i-1])/(b[i]-a[i]*c[i-1]);	

	x[n-1]=d[n-1];
	for (i=n-2; i>-1; i--){
		x[i]=d[i]-c[i]*x[i+1];
	}
}

/*Flux balance equation solver, answer is recorded in b*/
void fluxbal(int n, double* pregbval, double* coeff, double* fracfax, double* mode, double* SA, double* oxcon, double* b){

	int i, j, k;

	/*define the matrix A*/
	double A[n][n];
	for (i=0; i<n; i++){
	for (j=0; j<n; j++){
		A[i][j]=0;
	}}

	for (i=0; i<n-1; i++){
		A[i][0]=1;
		A[i][(i+1)]=-1;
	}
	for (i=0; i<n; i++){
		A[(n-1)][(i)]=(mode[i])*SA[i]*oxcon[i]*coeff[i];
	}

	/*define right hand side b*/
	for (i=0; i<n-1; i++){
		b[i]=fracfax[i+1];
	}
	
	b[n-1]=0;
	for (i=0; i<n; i++){
		b[n-1] += (mode[i])*SA[i]*oxcon[i]*coeff[i]*pregbval[i];
	}

	/*print A and b
	for (i=0; i<n; i++){
	for (j=0; j<n; j++){
		printf("%2.14le\n",A[i][j]);
	}}
	for (j=0; j<n; j++){
		printf("%2.14le\n", b[j]);
	}*/

	/*print b calc components
	for (i=0; i<n; i++){
		printf("%2.14le\n",pregbval[i]);
	}	

	getchar();*/

	/*make system upper triangular*/
	double scale;
	int i1,j1;
	for (k=0; k<n; k++){

	   /*divide each element in the kth row by its leading element*/
	   scale=A[k][k];
	   for (i=k; i<n; i++){
	  	A[k][i]=A[k][i]/scale;
	   	b[k]=b[k]/scale;
	   }

	   /*now subtract row from each one below*/
	   for (i=k+1; i<n; i++){
		scale=A[i][k];
		b[i]=b[i]-scale*b[k];
	   	for (j=k; j<n; j++){
			A[i][j]=A[i][j]-scale*A[k][j];
	   }}

	}

	/*put into row echolon form*/
	for (k=n-1; k>0; k--){
	    b[k-1]=b[k-1]-b[k]*A[k-1][k];
	}
}



#define MAXCHAR 100
int runforward(char* param_loc, char* cool_loc, char* Xsave_loc, char* Ysave_loc){

	double pi = acos(-1.0);
	int genint;
	double gendouble;
	double gendouble2;


	/*read in paramater file*/
	char line[MAXCHAR];
	FILE *param_file;

	param_file = fopen(param_loc, "r");
	if (param_file == NULL){
		printf("Could not open file %s\n", param_loc);
		return 0;
	}



	/*Using parameter file, read in all model characteristics.
	  This allows arbitrary number of minerals.*/
	char *ans;
	char *junk;

	double ttot;
	double dt;
	double WRd180;
	double Tstart;
	double Tend;
	double deltat;
	int nummin;
	int de=100;
        double mult_dt=1;
        //printf("\n%f\n",mult);


	/*get number of minerals and other global parameters*/
	genint=1;
	while(genint<8 && fgets(line, sizeof line, param_file) != NULL){	

	if(genint == 1){
		strtok_r(line, ",",&ans);
		strtok_r(ans, "\n",&junk);
		nummin = strtol(ans,NULL,10);
		//printf("%i\n",nummin);
	}

	if(genint == 3){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		WRd180 = strtod(ans, NULL);
		//printf("%f\n",WRd180);
	}

	if(genint == 4){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		ttot = strtod(ans, NULL);
		//printf("%f\n",ttot);
	}

	if(genint == 5){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		Tstart = strtod(ans, NULL);
		//printf("%f\n",Tstart);
	}

	if(genint == 6){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		dt = strtod(ans, NULL);
		dt=5e-4/mult_dt;
		deltat=dt*3.1536e+13;
		//printf("%f\n",dt);
	}

	if(genint == 7){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		Tend = strtod(ans, NULL);
		//printf("%f\n",Tend);
	}

	genint ++;
	}

	/*now that we know number of minerals declare all variables*/
	double mode[nummin];
	int shape[nummin]; /*1 sphere, 2 slab*/
	double L[nummin];
	double w[nummin];
	double r[nummin];

	double d180[nummin];
	double Afrac[nummin];
	double Bfrac[nummin];
	double Cfrac[nummin];
	double D0[nummin];
	double Q[nummin];
	double D[nummin];
	double fracfax[nummin];
	double oxcon[nummin];
	double R=8.3144621;


	double dx[nummin];//distance step will be calculated
	int gb[nummin]; //so will the number of grid nodes
	int maxgb=2*de+1;
	double SA[nummin]; //surface area

	/*now finish setting all individual mineral properties*/
	while(fgets(line, sizeof line, param_file) != NULL){

	
	if ((genint-9)%11 == 0 && (genint-9)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		mode[(genint-9)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",mode[(genint-9)/11]);
	}

	if ((genint-10)%11 == 0 && (genint-10)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);

		if (strcmp(ans,"Spherical") == 0){shape[(genint-10)/11]=1;}
		if (strcmp(ans,"Slab") == 0){shape[(genint-10)/11]=2;}

		//printf("%i\n",shape[(genint-9)/11]);
	}

	if ((genint-11)%11 == 0 && (genint-11)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		r[(genint-11)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",r[(genint-11)/11]);
	}

	if ((genint-12)%11 == 0 && (genint-12)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		w[(genint-12)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",w[(genint-12)/11]);
	}

	if ((genint-13)%11 == 0 && (genint-13)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		Afrac[(genint-13)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",Afrac[(genint-13)/11]);
	}

	if ((genint-14)%11 == 0 && (genint-14)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		Bfrac[(genint-14)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",Bfrac[(genint-14)/11]);
	}

	if ((genint-15)%11 == 0 && (genint-15)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		Cfrac[(genint-15)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",Cfrac[(genint-15)/11]);
	}

	if ((genint-16)%11 == 0 && (genint-16)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		D0[(genint-16)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",D0[(genint-16)/11]);
	}

	if ((genint-17)%11 == 0 && (genint-17)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		Q[(genint-17)/11] = strtod(ans, NULL);
		//printf("%2.16le\n",Q[(genint-17)/11]);
	}

	if ((genint-18)%11 == 0 && (genint-18)/11 < nummin){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		oxcon[(genint-18)/11] = strtod(ans, NULL);
		//printf("%f\n",oxcon[(genint-18)/11]);
	}

	
	//getchar();
	genint++;
	}

	/*read in cooling history file*/
	FILE *cool_file;

	cool_file = fopen(cool_loc, "r");
	if (cool_file == NULL){
		printf("Could not open file %s\n", cool_loc);
		return 0;
	}

	int cooln=0;
	double cool_hist[100][100];
	while(fgets(line, sizeof line, cool_file) != NULL){
		strtok_r(line,",",&ans);
		strtok_r(ans,"\n",&junk);
		
		cool_hist[cooln][0] = strtod(line, NULL);
		cool_hist[cooln][1] = strtod(ans, NULL)+273;		

		//printf("%2.16le - %2.16le\n",cool_hist[cooln][0],cool_hist[cooln][1]);
		cooln++;
	}
	ttot=cool_hist[cooln-1][0];
	int tend = (int) ceil(ttot/dt);
		


	/*normalize mineral modes to 1 if not already normalized*/
	gendouble=0;
	for (genint=0; genint<nummin; genint++){
		gendouble += mode[genint];
	}
	for (genint=0; genint<nummin; genint++){
		mode[genint]=mode[genint]/gendouble;
	}

	/*calculate distance step for each mineral*/
	for (genint=0; genint<nummin; genint++){
		L[genint]=2*r[genint];
		dx[genint]=r[genint]/de;
		if (shape[genint]==1){gb[genint]=de+1;}
		if (shape[genint]==2){gb[genint]=2*de+1;}
		//if (gb[genint]>maxgb){maxgb=gb[genint];}
	}



	/*convert all input micron values to cm*/
	for (genint=0; genint<nummin; genint++){
		L[genint]=L[genint]*(1e-4);
		w[genint]=w[genint]*(1e-4);
		r[genint]=r[genint]*(1e-4);
		dx[genint]=dx[genint]*(1e-4);
	}

	/*calculate mineral surface area*/
	for (genint=0; genint<nummin; genint++){
		if (shape[genint] == 1){
			SA[genint] = 4*pi*r[genint]*r[genint];
		}
	
		if (shape[genint] == 2){
			SA[genint] = 2*L[genint]*w[genint];
		}
		//printf("%2.16le\n", SA[genint]);
	}

	/* initialize the model solver */
	double d180mon=WRd180;
	for (genint=0; genint<nummin; genint++){
		fracfax[genint]=Afrac[genint]+(Bfrac[genint]*1e3)/cool_hist[0][1] \
		+(Cfrac[genint]*1e6)/pow(cool_hist[0][1],2);

		d180mon += mode[genint]*fracfax[genint];
		//printf("%f\n",d180mon);
	}



	double Told[nummin][maxgb];
	double gbvalinit[nummin];
	for (genint=0; genint<nummin; genint++){
		gbvalinit[genint]=d180mon-fracfax[genint];
	}

	for (int m=0; m<nummin; m++){
	for (genint=0; genint<gb[m]; genint++){
		Told[m][genint]=gbvalinit[m];
	}}
		
	/*This section can be used to output current solution
	if (0==0){
		for (genint=0; genint<maxgb; genint++){
			printf("\n");
			for (int m=0; m<nummin; m++){
				printf("%2.16le   ",Told[m][genint]);
			}
		}

		getchar();
	}*/

/*--- begin the fully implicit solution solver ---*/

	double Tnew[nummin][maxgb];

	double gbval[nummin];
	double pregbval[nummin];
	double coeff[nummin];

	double DTdt;
	double T=cool_hist[0][1];

	/*these arrays are much longer so we don't want them stored on the stack*/
	double *time = (double *) malloc(tend*sizeof(double));
	double *Temphx = (double *) malloc(tend*sizeof(double));

	double *a = (double *) malloc(maxgb*sizeof(double));
	double *b = (double *) malloc(maxgb*sizeof(double));
	double *c = (double *) malloc(maxgb*sizeof(double));
	double *d = (double *) malloc(maxgb*sizeof(double));

	double *a_copy = (double *) malloc(nummin*maxgb*sizeof(double));
	double *b_copy = (double *) malloc(nummin*maxgb*sizeof(double));
	double *c_copy = (double *) malloc(nummin*maxgb*sizeof(double));
	double *d_copy = (double *) malloc(nummin*maxgb*sizeof(double));

	/*initialize arrays*/
	for (int m=0; m<nummin; m++){
	for (int genint=0; genint<gb[m]; genint++){
		if (shape[m] == 1){ //spherical
			for (int genint=0; genint<gb[m]; genint++){
				a_copy[m*maxgb+genint]=((double) genint)/(genint+1);
				b_copy[m*maxgb+genint]=-(dx[m]*dx[m])/(deltat);
				c_copy[m*maxgb+genint]=((double) genint+2)/(genint+1);
			}

		}

		if (shape[m] == 2){// slab
			for (int genint=0; genint<gb[m]; genint++){
				a_copy[m*maxgb+genint]=1;
				b_copy[m*maxgb+genint]=-(dx[m]*dx[m])/(deltat);
				c_copy[m*maxgb+genint]=1;
			}
		}

		a_copy[m*maxgb+gb[m]-1]=2;
		c_copy[m*maxgb+0]=2;		
	}}


	double DTprev=0;
	for (int t=0; t<tend; t++){

	/*calculate the current change in temperature rate (cooling rate), and update temperature*/
	genint=1;
	while (cool_hist[genint][0]<ttot*((double)t/tend) && genint<cooln){genint++;}
	DTdt=-(cool_hist[genint][1]-cool_hist[genint-1][1])/(cool_hist[genint][0]-cool_hist[genint-1][0]);
	T=T-DTdt*dt;

	/*update fractionation factors and calculate current diffusivity*/
	for (genint=0; genint<nummin; genint++){
		fracfax[genint]=Afrac[genint]+(Bfrac[genint]*1e3)/T+(Cfrac[genint]*1e6)/pow(T,2);
		D[genint]=D0[genint]*exp(-Q[genint]/(R*T));
		coeff[genint]=D[genint]/dx[genint];
	}

	/*for each mineral set up the Crank-Nicholson matrix and solver*/
	for (int m=0; m<nummin; m++){
		memcpy(a,&a_copy[m*maxgb],maxgb*sizeof(double));
		memcpy(c,&c_copy[m*maxgb],maxgb*sizeof(double));

		for (int genint=0; genint<gb[m]; genint++){
			b[genint]=-2+b_copy[m*maxgb+genint]/D[m];
			d[genint]=b_copy[m*maxgb+genint]*(Told[m][genint]/D[m]);
		}
		thomas_alg(gb[m], a, b, c, d, &Tnew[m][0]);
	}

	/*reset pregrain values and solve flux balance equation*/
	for (int m=0; m<nummin; m++){
		pregbval[m]=Tnew[m][gb[m]-2];
	}

	fluxbal(nummin, pregbval, coeff, fracfax, mode, SA, oxcon, &gbval[0]);
	
	/*if(t>50){
	print current old
	for (int m=91; m<102; m++){
		printf("%2.16lf\n",Told[3][m]);
	}
	getchar();
	}*/



	/*store old result in new result*/
	for (int m=0; m<nummin; m++){
		Tnew[m][gb[m]-1]=gbval[m];
		if (shape[m] == 2){Tnew[m][0]=gbval[m];}

		for (genint=0; genint<gb[m]; genint++){
			Told[m][genint]=Tnew[m][genint];
			time[t]=t*dt;
			Temphx[t]=T;
		}
	}





	} // end of t loop


	/*create X and Y matrices*/
	double *X = (double *) malloc(maxgb*nummin*sizeof(double));
	double *Y = (double *) malloc(maxgb*nummin*sizeof(double));

	for (int m=0; m<nummin; m++){
		if (shape[m] == 2){
		for (genint=0; genint<gb[m]; genint++){
			Y[m*maxgb+genint]=Told[m][genint];

		}}
		if (shape[m] == 1){
		for (genint=0; genint<gb[m]; genint++){
			Y[m*maxgb+genint]=Told[m][gb[m]-1-genint];
			Y[m*maxgb+2*gb[m]-2-genint]=Told[m][gb[m]-1-genint];
		}}
	}

	
	for (int m=0; m<nummin; m++){
	X[m*maxgb]=0;
	for (genint=1; genint<maxgb; genint++){
		X[m*maxgb+genint]=X[m*maxgb+genint-1]+dx[m]*(1e4);
	}}

	/*now write X data to file*/
	FILE *f = fopen(Xsave_loc, "w");

	fprintf(f,"%2.16e",X[0]);
	for (int m=1; m<nummin; m++){
		fprintf(f,",%2.16e",X[m*maxgb]);
	}

	for (genint=1; genint<maxgb; genint++){
		fprintf(f,"\n%2.16e",X[0+genint]);
		for (int m=1; m<nummin; m++){
			fprintf(f,",%2.16e",X[m*maxgb+genint]);
		}
	}
	fclose(f);

	/*now write Y data to file*/
	f = fopen(Ysave_loc, "w");

	fprintf(f,"%lf",Y[0]);
	for (int m=1; m<nummin; m++){
		fprintf(f,",%2.16e",Y[m*maxgb]);
	}

	for (genint=1; genint<maxgb; genint++){
		fprintf(f,"\n%2.16e",Y[0+genint]);
		for (int m=1; m<nummin; m++){
			fprintf(f,",%2.16e",Y[m*maxgb+genint]);
		}
	}
	fclose(f);





	/*This section can be used to output final solution
	for (genint=0; genint<maxgb; genint++){
		printf("\n");
		for (int m=0; m<nummin; m++){
			printf("%2.4f   ",X[m*maxgb+genint]);
		}

	}*/

	//printf("\n----------------------------------\n");
	/*This section can be used to output final solution
	for (genint=0; genint<maxgb; genint++){
		printf("\n");
		for (int m=0; m<nummin; m++){
			printf("%2.4f   ",Y[m*maxgb+genint]);
		}

	}*/
}

int main(int argc, char **argv){

	runforward(argv[1], argv[2], argv[3], argv[4]);
	
	//char* param_loc = "temp_param.txt";
	//char* cool_loc = "temp_cool2.txt";
	//runforward(param_loc,cool_loc,"0X.txt","0Y.txt");
	//printf("%s\n %s\n %s\n",argv[1],argv[2],argv[3]);
	
}






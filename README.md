# iccve2019_valmon
Please find here supplementary code for the paper: Online validity 
monitor for vehicle dynamics models; Stephan Rhode and Johannes 
von Keler; 2019 IEEE International Conference on Connected 
Vehicles and Expo (ICCVE)

    @InProceedings{Rhode2019,
      Title                    = {Online validity monitor for vehicle dynamics models},
      Author                   = {S. {Rhode} and J. {Von Keler}},
      Abstract                 = {This paper presents a method to measure the degree of validity of vehicle
            dynamics models during run time in a computational efficient way. The
            method is called online validity monitor and is constructed as follows.
            First, the characteristic validation error distribution of a vehicle
            dynamics model is stored. Second, during run time, an error distribution is
            recorded via a circular buffer. Third, the distance between stored and run
            time error distribution is taken as a measure to detect if the model
            operates in its validated domain.}
      Booktitle                = {2019 IEEE International Conference on Connected Vehicles and Expo (ICCVE)},
      Year                     = {2019},
      Month                    = {Nov},
      Pages                    = {1-6},

      Doi                      = {10.1109/ICCVE45908.2019.8965162},
      ISSN                     = {2378-1289},
      Keywords                 = {Model validation;online;vehicle dynamics;Jensen-Shannon divergence}
    }

## Purpose
This software is a research prototype, solely developed for and 
published as part of the publication. It will neither be maintained 
nor monitored in any way.

## Requirements, how to use, install
You need a python environment with toolboxes defined in 
[requirements.txt](requirements.txt). You can either use pip
or conda to create this environment. Then, simply run `experiment.py` 
to reproduce result plots of the paper.

## License
This software is licensed under AGPL-3.0 license.

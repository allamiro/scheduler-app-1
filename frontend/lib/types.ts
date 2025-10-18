export type Doctor = {
  id: number;
  name: string;
  specialty: string;
  capacity: number;
};

export type Assignment = {
  id: number;
  date: string;
  assignment_type: string;
  doctor: Doctor;
};

export type Schedule = {
  id: number;
  title: string;
  week_start: string;
  assignments: Assignment[];
};

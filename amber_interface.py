from parmed import gromacs, amber
import sys
import subprocess
import os

def amber_inputs(topol, gro):
#Creates amber inputs from gromacs topology and corresponding .gro file. Example amber_inputs("topol.top","equilibrated.gro")
#uses parmed
	gmx_top = gromacs.GromacsTopologyFile(topol)
	gmx_gro = gromacs.GromacsGroFile.parse(gro)
	gmx_top.box = gmx_gro.box
	gmx_top.positions = gmx_gro.positions
	#gmx_top.velocities = gmx_gro.velocities

	for res in gmx_top.residues:
		if res.name=='TIP3':
			res.name='WAT'
			res.atoms[0].name='O'

	amb_prm = amber.ChamberParm.from_structure(gmx_top)
	amb_prm.write_parm("prmtop")
	amb_inpcrd = amber.AmberAsciiRestart("inpcrd", mode="w", hasbox=True)

	amb_inpcrd.coordinates = gmx_top.coordinates
	#amb_inpcrd.velocities = gmx_top.velocities
	amb_inpcrd.box = gmx_top.box
	amb_inpcrd.close()

def amber2grotraj():
#concanates amber trajectioris with name prod*.nc to gromacs prod.trr. Assumes an amber topology with name prmtop to be present 
#requires mdconvert to be installed
	subprocess.call(['cp', 'prmtop', 'prmtop.prmtop'])
	if os.path.exists("prod.trr"):
		os.system('rm prod.trr')
	subprocess.call(['mdconvert','prod*.nc','-t', 'prmtop.prmtop','-o', 'prod.trr'])	
	

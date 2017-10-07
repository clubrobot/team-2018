#ifndef __POSITIONCONTROLLER_H__
#define __POSITIONCONTROLLER_H__

#include "PeriodicProcess.h"
#include "Odometry.h"


class AbstractMoveStrategy;
/**
 * @brief Classe support des objets AbstractMoveStrategy.
 * 
 * PositionController est le support des AbstractMoveStrategy. C'est à dire qu'il permet de charger ou supprimer une stratégie.
 * Quand PositionController execute une stratégie de mouvement, il va l'executé tous les time_steps pour y obtenir de nouvelles vitesses à suivre.
 * PositionConstroller va égalemenr renseigné la position du robot à AbstractMoveStrategy chargée.
 * 
 * @return class PositionController : public PeriodicProcess { public: 
 */
class PositionController : public PeriodicProcess
{
public:
	/**
	 * @brief Constructeur de PositionController
	 * 
	 * Initialise les variables de PositionController à des valeurs neutre.
	 * 
	 */
	PositionController() : m_linVelKp(1), m_angVelKp(1), m_linVelMax(1000), m_angVelMax(2 * M_PI){}

	/**
	 * @brief Charge les nouvelles positions du robot.
	 * 
	 * Charge les nouvelles positions du robot pour les donner à une potentiel AbstractMoveStrategy chargée.
	 * 
	 * @param posInput Nouvelle objet Position représentant la position du robot.
	 */
	void setPosInput   (const Position& posInput)   {m_posInput    = posInput;}
	/**
	 * @brief Charge la position à atteindre.
	 * 
	 * Charge la position à atteindre avec une AbstractMoveStrategy.
	 * 
	 * @param posSetpoint
	 */
	void setPosSetpoint(const Position& posSetpoint){m_posSetpoint = posSetpoint;}

	void setThetaSetpoint(float theta){m_posSetpoint.theta = theta;}

	float getLinVelSetpoint() const {return m_linVelSetpoint;}
	float getAngVelSetpoint() const {return m_angVelSetpoint;}

	void setVelTunings(float linVelKp, float angVelKp) {m_linVelKp  = linVelKp;  m_angVelKp  = angVelKp;}
	void setVelLimits(float linVelMax, float angVelMax){m_linVelMax = linVelMax; m_angVelMax = angVelMax;}
	void setPosThresholds(float linPosThreshold, float angPosThreshold){m_linPosThreshold = linPosThreshold; m_angPosThreshold = angPosThreshold;}

	void setMoveStrategy(AbstractMoveStrategy& moveStrategy);

	bool getPositionReached();

	float getLinVelKp() const {return m_linVelKp;}
	float getAngVelKp() const {return m_angVelKp;}
	float getLinVelMax() const {return m_linVelMax;}
	float getAngVelMax() const {return m_angVelMax;}
	float getLinPosThreshold() const {return m_linPosThreshold;}
	float getAngPosThreshold() const {return m_angPosThreshold;}

	void load(int address);
	void save(int address) const;

private:

	virtual void process(float timestep);
	virtual void onProcessEnabling();

	// IO
	Position m_posInput;
	Position m_posSetpoint;

	float m_linVelSetpoint;
	float m_angVelSetpoint;

	// Engineering control tunings
	float m_linVelKp;
	float m_angVelKp;
	float m_linVelMax;
	float m_angVelMax;
	float m_linPosThreshold;
	float m_angPosThreshold;

	// Strategy Design Pattern
	AbstractMoveStrategy* m_moveStrategy;

	friend class AbstractMoveStrategy;
};

class AbstractMoveStrategy
{
protected:

	virtual void computeVelSetpoints(float timestep) = 0;
	virtual bool getPositionReached() = 0;

	const Position& getPosInput()    const {return m_context->m_posInput;}
	const Position& getPosSetpoint() const {return m_context->m_posSetpoint;}

	void setVelSetpoints(float linVelSetpoint, float angVelSetpoint){m_context->m_linVelSetpoint = linVelSetpoint; m_context->m_angVelSetpoint = angVelSetpoint;}

	float getLinVelKp() const {return m_context->m_linVelKp;}
	float getAngVelKp() const {return m_context->m_angVelKp;}
	float getLinVelMax() const {return m_context->m_linVelMax;}
	float getAngVelMax() const {return m_context->m_angVelMax;}
	float getLinPosThreshold() const {return m_context->m_linPosThreshold;}
	float getAngPosThreshold() const {return m_context->m_angPosThreshold;}

private:

	PositionController* m_context;

	friend class PositionController;
};

#endif // __POSITIONCONTROLLER_H__

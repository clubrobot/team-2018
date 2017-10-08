#ifndef __VELOCITYCONTROLLER_H__
#define __VELOCITYCONTROLLER_H__

#include "DifferentialController.h"

#include <math.h>

#define ENABLE_VELOCITYCONTROLLER_LOGS 0 // for debug purposes
#define VELOCITYCONTROLLER_LOGS_TIMESTEP 50e-3 // mm

/**
 * @brief Objet de controle de la vitesse.
 * 
 * VelocityController contrôle la vitesse à atteindre à partir de la vitesse que l'utilisateur veux atteindre.
 * VelocityController va appliquer une ramp d'accélération pour respecter une ramp d'accélération.
 * 
 */
class VelocityController : public DifferentialController
{
public:
	/**
	 * @brief Constructeur de VelocityController
	 * 
	 * Construteur de VelocityController qui initialise ces vairables sur des valeurs neutres.
	 * 
	 */
	VelocityController() : m_rampLinVelSetpoint(0), m_rampAngVelSetpoint(0), m_maxLinAcc(INFINITY), m_maxLinDec(INFINITY), m_maxAngAcc(INFINITY), m_maxAngDec(INFINITY), m_spinShutdown(true){}


	/**
	 * @brief Paramètre les accélérations max.
	 * 
	 * @param maxLinAcc Accélération linéaire en mm/s².
	 * @param maxAngAcc Accélération angulaire en rad/s².
	 */
	void setMaxAcc(float maxLinAcc, float maxAngAcc){m_maxLinAcc = maxLinAcc; m_maxAngAcc = maxAngAcc;}

	/**
	 * @brief Paramètre les décéleration max.
	 * 
	 * @param maxLinAcc Décélération linéaire en mm/s².
	 * @param maxAngAcc Décélération angulaire en rad/s².
	 */
	void setMaxDec(float maxLinDec, float maxAngDec){m_maxLinDec = maxLinDec; m_maxAngDec = maxAngDec;}
	/**
	 * @brief Change l'état de l'arret d'urgence.
	 *
	 * 
	 * @param Etat à appliquer à la variable spinShutdown.
	 */
	void setSpinShutdown(bool spinShutdown){m_spinShutdown = spinShutdown;}

	/**
	 * @brief Retourne l'accélération max linéaire.
	 * 
	 * @return Accélération en mm/s².
	 */
	float getMaxLinAcc() const {return m_maxLinAcc;}

	/**
	 * @brief Retourne l'accélération max angulaire.
	 * 
	 * @return Accélération en rad/s².
	 */
	float getMaxAngAcc() const {return m_maxAngAcc;}
	/**
	 * @brief Retourne la décélération max linéaire.
	 * 
	 * @return Décélération en mm/s².
	 */	
	float getMaxLinDec() const {return m_maxLinDec;}
	/**
	 * @brief Retourne la décélération max angulaire.
	 * 
	 * @return Décélération en rad/s².
	 */
	float getMaxAngDec() const {return m_maxAngDec;}
	/**
	 * @brief Retourne l'état de spinShutDown
	 * 
	 * @return true Si le robot est bloqué par un obstacle.
	 * @return false Si le robot n'est pas bloqué.
	 */
	bool getSpinShutdown() const {return m_spinShutdown;}

	/**
	 * @brief Charge les paramètres.
	 * 
	 * Charge les derniers paramètres sauvegarder (les acc et dec) dans l'Arduino.
	 * 
	 * @param Adresse à utiliser.
	 */
	void load(int address);
	/**
	 * @brief Sauvegarde les paramètres.
	 * 
	 * Sauvegarde les paramètres actuellement chargés.
	 * 
	 * @param Adresse à utiliser.
	 */
	void save(int address) const;

protected:
	/**
	 * @brief Calcul la vitesse à atteindre.
	 * 
	 * Calcul les nouvelles vitesse à atteindre pour respecter les contraites d'accélérations.
	 * 
	 * @param stepSetpoint Vitesse à atteindre.
	 * @param input Vitesse actuel
	 * @param rampSetpoint 
	 * @param maxAcc
	 * @param maxDec
	 * @param timestep
	 * 
	 * @return float
	 */
	float genRampSetpoint(float stepSetpoint, float input, float rampSetpoint, float maxAcc, float maxDec, float timestep);

	virtual void process(float timestep);
	virtual void onProcessEnabling();

	float m_rampLinVelSetpoint; // in mm/s (no longer w/e unit)
	float m_rampAngVelSetpoint; // in rad/s (no longer w/e unit)
	float m_maxLinAcc; // always positive, in mm/s^2
	float m_maxLinDec; // always positive, in mm/s^2
	float m_maxAngAcc; // always positive, in rad/s^2
	float m_maxAngDec; // always positive, in rad/s^2
	bool m_spinShutdown;

#if ENABLE_VELOCITYCONTROLLER_LOGS
	friend class VelocityControllerLogs;
#endif // ENABLE_VELOCITYCONTROLLER_LOGS
};

#if ENABLE_VELOCITYCONTROLLER_LOGS
class VelocityControllerLogs : public PeriodicProcess
{
public:

	void setController(const VelocityController& controller){m_controller = &controller;}

protected:

	virtual void process(float timestep);

	const VelocityController* m_controller;
};
#endif // ENABLE_VELOCITYCONTROLLER_LOGS

#endif // __VELOCITYCONTROLLER_H__

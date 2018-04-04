#include "SensorListener.h"

SensorListener::SensorListener() : m_sensor(0), m_timestep(0.0), m_clock(), m_mesures()
{
    m_clock.restart();
    for(int i=0;i<LISTENER_MAX_HISTORY;i++) m_oldStd[i] = m_oldVar[i] = -1;
}


SensorListener::attach(UltrasonicSensor* sensor, int timestep)
{
    m_sensor  = sensor;
    m_interTimestep = timestep;
}

SensorListener::process(float timestep)
{
    if(m_mesures.count()<LISTENER_MAX_MESURE) m_mesures.enqueue(m_sensor->getMesure());

    if(m_internClock.getElapsedTime()>m_interTimestep*0.001)
    {
        //Compute std and var
        int nb_measure = m_measure.count();
        float std = 0.0, var  =0.0;
        float m;
        for(int i=0;i<nb_measure;i++)
        {
            std += m = m_measure.dequeue();
            m_measure.enqueue(m);
        }
        std /= nb_measure;
        for(int i=0;i<nb_measure;i++)
        {
            var += (m_measure.dequeue()-std)**2;
        }
        var /= nb_measure;

        storeStd(std);
        storeVar(var);


        m_internClock.reset();
    }



}

SensorListener::storeStd(float std)
{
    for(int i=0;i<LISTENER_MAX_HISTORY-1;i++) m_oldStd[i+1] = m_oldStd[i];
    m_oldStd[0] = std;

}


SensorListener::storeVar(float var)
{
    for(int i=0;i<LISTENER_MAX_HISTORY-1;i++) m_oldVar[i+1] = m_oldVar[i];
    m_oldVar[0] = std;

}


SensorListener::getStd(int delta){ return m_oldStd[delta];}

SensorListener::getVar(int delta){ return m_oldVar[delta];}

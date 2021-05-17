using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace PhilosophyProblemDrei
{
  internal class Philosoph
  {
    public int PersonNo { get; }

    public Semaphore Semaphore { get; } = new Semaphore(0, 2);

    public PhilosopherState CurrentState { get; set; } = PhilosopherState.THINKING;

    public Philosoph Left { get; set; }

    public Philosoph Right { get; set; }

    public Philosoph Top { get; set; }

    public IReadOnlyList<Philosoph> AllNeighbors => new[] { Left, Right, Top }.Where(x => x != null).ToList();

    public Philosoph(int no)
    {
      PersonNo = no;
    }

    public void TakeForks()
    {
      Program.Mutex.WaitOne();
      Program.Log("Philosoph {0} is taking forks", PersonNo);
      CurrentState = PhilosopherState.HUNGRY;
      Test();
      Program.Mutex.ReleaseMutex();
      Semaphore.WaitOne();
    }

    public void PutForks()
    {
      Program.Mutex.WaitOne();
      CurrentState = PhilosopherState.THINKING;
      foreach (var neighbor in AllNeighbors)
      {
        neighbor.Test();
      }
      Program.Mutex.ReleaseMutex();
    }

    public void Eat()
    {
      Program.Log("Philosoph {0} is eating", PersonNo);
      Thread.Sleep(Program.SLEEP_AMOUNT);
      Program.Log("Philosoph {0} finished eating", PersonNo);
    }

    public void Think()
    {
      Program.Log("Philosoph {0} is thinking", PersonNo);
      Thread.Sleep(Program.SLEEP_AMOUNT);
      Program.Log("Philosoph {0} finished thinking", PersonNo);
    }

    public void SetNeighbors(Philosoph left, Philosoph right, Philosoph top)
    {
      Left = left;
      Right = right;
      Top = top;
    }

    public void Test()
    {
      if (CurrentState == PhilosopherState.HUNGRY && AllNeighbors.All(s => s.CurrentState != PhilosopherState.EATING))
      {
        CurrentState = PhilosopherState.EATING;
        Semaphore.Release();
      }
    }
  }
}

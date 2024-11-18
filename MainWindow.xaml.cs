using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Input;
using Nefarius.ViGEm.Client;
using Nefarius.ViGEm.Client.Targets;
using InputSimulatorStandard;
using System.Timers;
using System.Windows.Interop;


namespace VirtualController;

public partial class MainWindow : Window
{
    private readonly InputSimulator _inputSimulator = new InputSimulator();
    private ViGEmClient client;
    private IXbox360Controller controller;

    [DllImport("user32.dll")]
    private static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    private static extern void SetForegroundWindow(IntPtr hWnd);

    private IntPtr _lastFocusedWindow;

    public MainWindow()
    {
        InitializeComponent();
        Loaded += InitializeVirtualController;
        Closed += MainWindow_Closed;
    }
    private void InitializeVirtualController(object? sender, EventArgs e)
    {

        try
        {
            client = new ViGEmClient();
            controller = client.CreateXbox360Controller();
            controller.Connect();
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Failed to initialize virtual controller: {ex.Message}");
        }
    }

    private void MainWindow_Closed(object? sender, EventArgs e)
    {
        controller?.Disconnect();
        client?.Dispose();
    }

    // A
    private void btnA_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        SetForegroundWindow(_lastFocusedWindow);
        _inputSimulator.Keyboard.KeyPress(InputSimulatorStandard.Native.VirtualKeyCode.LEFT);
    }

    // W
    private void btnW_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        SetForegroundWindow(_lastFocusedWindow);
        _inputSimulator.Keyboard.KeyPress(InputSimulatorStandard.Native.VirtualKeyCode.VK_W);
    }

    // S
    private void btnS_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        SetForegroundWindow(_lastFocusedWindow);
        _inputSimulator.Keyboard.KeyPress(InputSimulatorStandard.Native.VirtualKeyCode.RIGHT);
    }

    // D
    private void btnD_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        SetForegroundWindow(_lastFocusedWindow);
        _inputSimulator.Keyboard.KeyPress(InputSimulatorStandard.Native.VirtualKeyCode.VK_D);
    }

    //drag
    private void Grid_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        DragMove();
    }

}
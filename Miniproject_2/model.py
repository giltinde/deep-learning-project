import math
import torch
torch.set_grad_enabled(False)

# --------------------- Module ---------------------

class Module(object):
    """
    Module class defining model architecture

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    param()
        Returns the list of trainable parameters
    """
    
    def __init__(self):
        """Constructor  

        Parameters
        ----------
        params : ?
            Parameters
        """
        pass
    
    def forward(self, *input):
        """Runs the forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying the module
        """
        raise NotImplementedError
        
    def backward(self, *gradwrtoutput):
        """Runs the backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the module's input
        """
        raise NotImplementedError 
        
    def param(self):
        """Returns the trainable parameters of the model

        Returns
        -------
        list
            The list of trainable parameters
        """
        return []

# ------------------- Sequential -------------------

class Sequential(Module):
    """
    Sequential model architecture class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    param()
        Returns the list of trainable parameters
    """
    
    def __init__(self, *modules):
        """Sequential constructor 
              
        Parameters
        ----------
        modules : Module
            Variable length list of modules
        """
        super().__init__()
        self.modules = list(modules)
        self.params = []
        for module in self.modules:
            for param in module.param():
                self.params.append(param)
    
    def forward(self, *input):
        """Sequential forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying the sequential model
        """
        forward_data = input[0].clone()
        for module in self.modules:
            forward_data = module.forward(forward_data)
        return forward_data
        
        
    def backward(self, *gradwrtoutput):
        """Sequential backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the module's input
        """
        backward_data = gradwrtoutput[0].clone()
        for module in reversed(self.modules):
            backward_data = module.backward(backward_data) 
        
    def param(self):
        """Returns the trainable parameters of the sequential model

        Returns
        -------
        list
            The list of trainable parameters
        """
        return self.params

# --------------------- Layers --------------------- 

class Linear(Module):
    """
    Linear layer class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    param()
        Returns the list of trainable parameters
    """
    
    def __init__(self, input_size, output_size, init_val=None):
        """Convolution constructor
        
        Parameters
        ----------
        input_size : int
            Size of each input sample
        output_size : int
            Size of each input sample
        init_val: float
            Default value of all weights (default is None)
        """
        super().__init__()
        self.Weight = torch.empty(input_size, output_size)
        self.bias = torch.empty(output_size)
        self.gradW = torch.empty(input_size, output_size)
        self.gradb = torch.empty(output_size)
        self.reset_params(input_size, init_val)
    
    def forward(self, *input):
        """Linear layer forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying convolution
        """
        self.input = input[0].clone()
        return self.input.mm(self.Weight).add(self.bias)
        
    def backward(self, *gradwrtoutput):
        """Linear layer backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the input
        """
        grad = gradwrtoutput[0].clone()
        self.gradW.add_(self.input.t().mm(grad))
        self.gradb.add_(grad.sum(0))
        return grad.mm(self.Weight.t()) 
        
    def param(self):
        """Returns the trainable parameters of the linear layer

        Returns
        -------
        list
            The list of trainable parameters
        """
        return [(self.Weight, self.gradW), (self.bias, self.gradb)]

    def reset_params(self, input_size, init_val=None):
        """Resets the trainable parameters of the linear layer"""
        if init_val is not None:
            self.Weight.fill_(init_val)
            self.bias.fill_(init_val)
        else:
            stdv = 1. / math.sqrt(input_size)
            self.Weight = self.Weight.uniform_(-stdv, stdv)
            self.bias = self.bias.uniform_(-stdv, stdv) 
        self.gradW.zero_()
        self.gradb.zero_()

def make_tuple(value, repetitions=2):
    return value if type(value) is tuple else tuple(value for _ in range(repetitions))

class Conv2d(Module):
    """
    Convolutional layer class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    param()
        Returns the list of trainable parameters
    """    
    def __init__(self, in_channels, out_channels, kernel_size, stride,
                 padding, dilation, use_bias=True):
        """Convolution constructor
        
        Parameters
        ----------
        params : ?
            Parameters
        """
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = make_tuple(kernel_size)
        self.stride = make_tuple(stride)
        self.padding = padding
        self.dilation = dilation
        self.use_bias = use_bias
        self.Weighteight = torch.empty(out_channels, in_channels, kernel_size[0], kernel_size[1])
        self.biasias = torch.empty(out_channels)
        self.reset_params()
    
    def forward(self, *input):
        """Convolutional layer forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying convolution
        """
        raise NotImplementedError
        
    def backward(self, *gradwrtoutput):
        """Convolutional layer backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the input
        """
        raise NotImplementedError 
        
    def param(self):
        """Returns the trainable parameters of the convolutional layer

        Returns
        -------
        list
            The list of trainable parameters
        """
        return []   

    def reset_params(self):
        """Resets the trainable parameters of the convolutional layer"""
        for k in self.kernel_size:
            n *= k
        stdv = 1. / math.sqrt(n)
        self.Weighteight.uniform_(-stdv, stdv)
        if self.biasias is not None:
            self.biasias.uniform_(-stdv, stdv)  

class NearestUpsampling(Module):
    """
    Upsampling layer class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    param()
        Returns the list of trainable parameters
    """    
    def __init__(self):
        """Upsampler constructor
        
        Parameters
        ----------
        params : ?
            Parameters
        """
        raise NotImplementedError
    
    def forward(self, *input):
        """Upsampling layer forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying upsampling
        """
        raise NotImplementedError
        
    def backward(self, *gradwrtoutput):
        """Upsampling layer backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the module's input
        """
        raise NotImplementedError 
        
    def param(self):
        """Returns the trainable parameters of the upsampling layer

        Returns
        -------
        list
            The list of trainable parameters
        """
        return []  

# --------------- Activation functions ------------- 

class ReLU(Module):
    """
    ReLU activation function class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    """
    
    def __init__(self):
        """ReLU constructor """
        super().__init__()
        self.input = None
    
    def forward(self, *input):
        """ReLU forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying the ReLU function
        """
        self.input = input[0].clone()
        return self.input.clamp(0)
        # return input[0].relu() # (or just call relu(), is this allowed?)
        
    def backward(self, *gradwrtoutput):
        """ReLU backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the module's input
        """
        backward = self.input.sign().clamp(0)
        # backward = self.input.relu().sign() (or just call relu(), is this allowed?)
        return backward.mul(gradwrtoutput[0])

class Sigmoid(Module):
    """
    Sigmoid activation function class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    """
    
    def __init__(self):
        """Sigmoid constructor 
              
        Parameters
        ----------
        params : ?
            Parameters
        """
        super().__init__()
        self.input = None
    
    def forward(self, *input):
        """Sigmoid forward pass

        Parameters
        ----------
        input : torch.tensor
            The input

        Returns
        -------
        torch.tensor
            The result of applying the sigmoid function
        """
        self.input = input[0].clone()
        return input[0].sigmoid() # Using sidmoid() here, is this allowed?
        
    def backward(self, *gradwrtoutput):
        """Sigmoid backward pass

        Parameters
        ----------
        gradwrtoutput : torch.tensor
            The gradients wrt the module's output

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the module's input
        """
        backward = self.input.sigmoid() * (1 - self.input.sigmoid()) # Using sidmoid() here, is this allowed?
        return backward.mul(gradwrtoutput[0])

# ----------------------- Loss --------------------- 

class MSE(Module):
    """
    MSE loss class

    Methods
    -------
    forward(input)
        Runs the forward pass
    backward(gradwrtoutput)
        Runs the backward pass
    """
    
    def __init__(self):
        """MSE loss constructor
              
        Parameters
        ----------
        params : ?
            Parameters
        """
        super().__init__()
        self.error = None
        self.num_samples = None
    
    def forward (self, prediction, target):
        """MSE loss forward pass

        Parameters
        ----------
        prediction : torch.tensor
            The predicted values
        target : torch.tensor
            The ground truth values

        Returns
        -------
        torch.tensor
            The result of applying the MSE
        """      
        self.error = prediction - target
        self.num_samples = prediction.size(0)        
        return self.error.pow(2).mean()
        
    def backward(self):
        """MSE loss backward pass

        Returns
        -------
        torch.tensor
            The gradient of the loss wrt the module's input
        """
        return (2.0 / self.num_samples) * self.error 

# -------------------- Optimizer ------------------- 

class SGD():
    """
    Stochastic gradient descent (SGD) class

    Methods
    -------
    step()
        Perform a SGD step
    zero_grad()
        Reset the trainable parameter gradients to zero
    """
    
    def __init__(self, params, lr):
        """SGD constructor
              
        Parameters
        ----------
        params : iterable
            Iterable of parameters to optimize
        lr: float
            Learning rate
        """
        self.params = params
        self.lr = lr
    
    def step(self):
        """Perform a SGD step"""
        for param, grad  in self.params:
            if (param is not None) and (grad is not None):
                param.sub_(grad, alpha=self.lr)
        
    def zero_grad(self):    
        """Reset the trainable parameter gradients to zero"""
        for param, grad in self.params:
            if (param is not None) and (grad is not None):
                grad.zero_()